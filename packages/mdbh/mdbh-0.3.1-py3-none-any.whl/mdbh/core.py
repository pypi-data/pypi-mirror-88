# -*- coding: utf-8 -*-1.3
# Copyright (C) 2020  The MDBH Authors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import configparser
from pathlib import Path
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import gridfs
import pandas as pd
from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo.database import Collection
from pymongo.database import Database

from mdbh import caching


def get_uri(conf_path: Union[Path, str],
            db_name: str) -> str:
    """Creates MongoDB connection URI from configuration file
    and database name.

    Args:
        conf_path: Path to the .mongo.conf configuration file.

        db_name: Name of the database to connect to.

    Returns:
        uri, MongoDB connection URI.
    """
    # Get path
    p = Path(conf_path).expanduser().absolute()

    if not p.exists():
        raise ValueError(f"Path {p} doest not exist.")

    # Load MongoDB configuration
    config = configparser.ConfigParser()
    config.read(p)

    server = config['SERVER']['ip']
    port = config['SERVER']['port']

    if 'username' in config['USER'].keys() and 'password' in config['USER'].keys():
        user = config['USER']['username']
        pw = config['USER']['password']

        if "auth" in config['USER'].keys():
            auth = config['USER']['auth']
        else:
            auth = "SCRAM-SHA-1"

        if "auth_db" in config['USER'].keys():
            auth_db = config['USER']['auth_db']
        else:
            auth_db = "admin"

        uri = f"mongodb://{user}:{pw}@{server}:{port}/{db_name}?authSource={auth_db}&authMechanism={auth}"

    else:
        print("No username and password specified.")
        uri = f"mongodb://{server}:{port}/{db_name}"

    return uri


def get_conf_databases(conf_path: Union[Path, str]) -> List[str]:
    """Get the name of databases specified in .mongo.conf config file.
    If none specified, uses "sacred" as default.

    Args:
        conf_path: Path to the .mongo.conf configuration file.

    Returns:
        List of Sacred databases.

    """
    # Get path
    p = Path(conf_path).expanduser().absolute()

    if not p.exists():
        raise ValueError(f"Path {p} doest not exist.")

    # Load MongoDB configuration
    config = configparser.ConfigParser()
    config.read(p)

    if 'DATABASES' not in config.keys():
        return ["sacred"]

    return [db for db in config['DATABASES'].values()]


def get_client(conf_path: Union[Path, str],
               db_name: str = "sacred") -> MongoClient:
    """Get a MongoClient using the specified configuration."""

    uri = get_uri(conf_path, db_name)
    return MongoClient(uri)


def get_mongodb(conf_path: Union[Path, str],
                db_name: str = "sacred") -> Database:
    """Get a MongoDB Database.

    Args:
        conf_path: Path to MongoDB configuration file.

        db_name: Name of the database.

    Returns:
        A PyMongo Database instance.

    """
    client = get_client(conf_path, db_name)
    return client.get_database()


def get_metric(db: Database, id: int, metric: str) -> dict:
    """Get metric from a Sacred experiment ID.

    Args:
        db: PyMongo Database instance.

        id: Run ID of experiment.

        metric: Name of the metric to get.

    Returns:
        dict, metric dictionary containing name, value, steps, etc.
    """
    if type(db) != Database:
        raise TypeError("db needs to be a PyMongo Database instance. "
                        "Use mdbh.get_mongodb")

    metrics = db.get_collection('metrics')
    return metrics.find_one({"run_id": id, "name": metric})


def _get_dataframe_query(db: Database,
                         query: dict,
                         collection: Union[str, Collection]) -> pd.DataFrame:
    """Get a DataFrame from a MongoDB query."""
    if type(db) != Database:
        raise TypeError("db needs to be a PyMongo Database instance. "
                        "Use mdbh.get_mongodb")
    # Query database and convert to DataFrame
    res = db[collection].find(query)
    df = pd.DataFrame(list(res))

    return df


def get_dataframe(db: Database,
                  ids: Optional[Union[int, List[int], Tuple[int, ...]]] = None,
                  include_artifacts: bool = False) -> pd.DataFrame:
    """Get all experiments from a Sacred Database in a DataFrame.
    Metrics and configurations are concatenated into a single DataFrame for
    convenience.

    Args:
        db: DataBase instance.

        ids: Optional list of run IDs to get. If None, all IDs are queried.

        include_artifacts: Whether to include a column for artifacts.
                           Artifacts can then be resolved via
                           :func:resolve_artifacts().

    Returns:
        DataFrame of the corresponding Database.
    """
    # Wrap ids into list
    ids = _wrap_ids(ids)

    # Get all metric and run logs
    query = {} if ids is None else {"run_id": {"$in": ids}}
    df_metric = _get_dataframe_query(db, query, "metrics")

    query = {} if ids is None else {"_id": {"$in": ids}}
    df_runs = _get_dataframe_query(db, query, "runs")

    # Set run_id (metrics), _id (runs) as index of DataFrames for later join
    df_metric.index = df_metric['run_id'].tolist()
    df_runs.index = df_runs['_id'].tolist()

    # Extract config dict into columns
    tmp = pd.DataFrame(df_runs['config'].tolist())
    tmp = tmp.rename(lambda x: f"config.{x}", axis=1)
    tmp.index = df_runs.index
    df_runs = pd.concat([df_runs, tmp], axis=1)

    # Extract experiment dict into columns
    tmp = pd.DataFrame(df_runs['experiment'].tolist())
    tmp = tmp.rename(lambda x: f"experiment.{x}", axis=1)
    tmp.index = df_runs.index
    df_runs = pd.concat([df_runs, tmp], axis=1)

    # Get all IDs
    ids = df_runs['_id'].unique().tolist()

    # Get metric column names
    metrics = df_metric['name'].unique().tolist()
    cols = [f"metrics.{i}" for i in metrics]

    # Create new DatFrame with extracted metrics
    df_metrics_full = pd.DataFrame(columns=["_id", *cols])
    for id in ids:
        df_metrics_full = df_metrics_full.append(pd.DataFrame([[id]], columns=['_id']))
        df_metrics_full.index = df_metrics_full['_id'].tolist()
        for col in metrics:
            try:
                df_metrics_full[f'metrics.{col}'][id] = df_metric[(df_metric["run_id"] == id) & (df_metric["name"] == col)]['values'].values[0]
            except IndexError:
                df_metrics_full[f'metrics.{col}'][id] = float("NaN")
            # Extract float values for test metrics
            if "test_" in col:
                try:
                    df_metrics_full[f'metrics.{col}'][id] = df_metrics_full[f'metrics.{col}'][id][0]
                except TypeError or IndexError:
                    pass

    # Clean up DataFrame
    df_m_del_cols = ['_id', ]
    df_r_del_cols = ['experiment', 'format', 'command', 'start_time', 'meta',
                     'resources', 'info', 'heartbeat',
                     'result', 'stop_time', 'fail_trace', 'captured_out',
                     'omniboard']

    if not include_artifacts:
        df_r_del_cols += ['artifacts']

    for i in df_m_del_cols:
        if i in df_metrics_full.columns.tolist():
            del df_metrics_full[i]

    for i in df_r_del_cols:
        if i in df_runs.columns.tolist():
            del df_runs[i]

    df = df_runs.join(df_metrics_full)
    df = df.rename(columns={'_id': 'id'})
    return df


def _get_artifact_content(db: Database, id: Union[str, ObjectId]) -> bytes:
    """Retrieves file content from GridFS by ObjectID. This corresponds to the way sacred saves artifacts.

    Args:
        db: DataBase instance.
        id: Object id (in string or ObjectID format)

    Returns:
        The file content as string
    """
    id = id if isinstance(id, ObjectId) else ObjectId(id)
    gr = gridfs.GridFS(db)
    return gr.get(id).read()


def resolve_artifacts(db: Database, df: pd.DataFrame) -> pd.DataFrame:
    """Maps the artifact column as retrieved from the database in
    get_df_full(..., return_artifacts=True) into a dictionary of the form
    {filename1: filecontent1, filename2:  filecontent2....}.

    Usage:

        df = mdbh.get_df_full(db, return_artifacts=True)
        df = mdbh.resolve_artifacts(db, df)

    Args:
        db: DataBase instance.
        df: The Dataframe with 'artifacts' column.

    Returns:
        The Dataframe with a transformed column
    """
    def map_artifacts(db: Database, x):
        return {artifact["name"]: _get_artifact_content(db, artifact["file_id"]) for artifact in x}
    df["artifacts"] = df["artifacts"].map(lambda x: map_artifacts(db, x))
    return df


def get_artifact_names(db: Database, id: int) -> List[str]:
    """Get the names of the artifacts from a run ID.

    Args:
        db: Database instance.
        id: Run ID.

    Returns:
        List of names of the ID's artifacts.
    """
    df = get_dataframe(db, [id], include_artifacts=True)
    return [a['name'] for a in df.loc[id]['artifacts']]


def get_artifact(db: Database,
                 id: int,
                 name: str,
                 force: bool = False):
    """Get path to artifact from database and run ID.
    The artifacts are cached by default.

    Args:
        db: DataBase instance.

        id: Run ID to get artifact from.

        name: Name of artifact to get.

        force: Whether to force downloading of the artifact, even if cached
                version is available.

    Returns:

    """
    def get_data():
        """Download artifact from MongoDB."""
        df = get_dataframe(db, [id], include_artifacts=True)
        artifacts = [a for a in df.loc[id]['artifacts'] if a['name'] == name]
        if len(artifacts) == 0:
            raise ValueError(f"No artifact found with name {name} for run ID {id}.")
        if len(artifacts) > 1:
            raise ValueError(f"Found more than one artifact with name {name} for run ID {id}.")
        artifact = artifacts[0]
        print(f"Downloading artifact from MongoDB.")
        return _get_artifact_content(db, artifact['file_id'])

    filename = f"{db.name}_{id}_{name}"
    return caching.get(filename, get_data)


def _wrap_ids(ids: Union[int, List[int], Tuple[int, ...]]) -> List[int]:
    """Wrap input ids into list of ints.

    Args:
        ids: Single or multiple ids.

    Returns:
        List of ids.
    """
    return list(ids) if isinstance(ids, (tuple, list, set)) else [ids]
