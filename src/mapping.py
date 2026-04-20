from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


LAT_CANDIDATES = ["latitude", "lat", "Latitude", "LATITUDE", "gps_latitude"]
LON_CANDIDATES = ["longitude", "lon", "Longitude", "LONGITUDE", "gps_longitude"]


def find_column(df, candidates):
    for col in candidates:
        if col in df.columns:
            return col

    lowered = {c.lower(): c for c in df.columns}
    for candidate in candidates:
        for lower_name, original_name in lowered.items():
            if candidate.lower() in lower_name:
                return original_name

    raise ValueError(
        f"Could not find a matching column. Available columns: {list(df.columns)}"
    )


def standardize_coordinates(df, label):
    lat_col = find_column(df, LAT_CANDIDATES)
    lon_col = find_column(df, LON_CANDIDATES)

    df = df.rename(columns={lat_col: "latitude", lon_col: "longitude"}).copy()
    df["event_type"] = label
    df = df.dropna(subset=["latitude", "longitude"])

    return df


def load_infrastructure_data(bridge_path, railjoint_path, turnout_path):
    bridge_df = pd.read_csv(bridge_path)
    railjoint_df = pd.read_csv(railjoint_path)
    turnout_df = pd.read_csv(turnout_path)

    bridge_df = standardize_coordinates(bridge_df, "Bridge")
    railjoint_df = standardize_coordinates(railjoint_df, "RailJoint")
    turnout_df = standardize_coordinates(turnout_df, "Turnout")

    return bridge_df, railjoint_df, turnout_df


def plot_infrastructure_map(bridge_df, railjoint_df, turnout_df, output_path):
    plt.figure(figsize=(12, 8))

    plt.scatter(
        bridge_df["longitude"],
        bridge_df["latitude"],
        label="Bridge",
        alpha=0.8,
        s=20
    )

    plt.scatter(
        railjoint_df["longitude"],
        railjoint_df["latitude"],
        label="RailJoint",
        alpha=0.8,
        s=20
    )

    plt.scatter(
        turnout_df["longitude"],
        turnout_df["latitude"],
        label="Turnout",
        alpha=0.8,
        s=20
    )

    plt.title("Track Infrastructure Map")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.legend()
    plt.grid(True)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


def load_gps_data(latitude_path, longitude_path, speed_path=None, satellites_path=None):
    """
    Load GPS latitude and longitude files and merge them into one DataFrame.

    These files are assumed to be single-column CSV files without headers.
    """
    lat_df = pd.read_csv(latitude_path, header=None)
    lon_df = pd.read_csv(longitude_path, header=None)

    lat_col = lat_df.columns[0]
    lon_col = lon_df.columns[0]

    gps_df = pd.DataFrame({
        "latitude": lat_df[lat_col],
        "longitude": lon_df[lon_col],
    })

    if speed_path is not None:
        speed_df = pd.read_csv(speed_path, header=None)
        gps_df["speed"] = speed_df.iloc[:, 0]

    if satellites_path is not None:
        sat_df = pd.read_csv(satellites_path, header=None)
        gps_df["satellites"] = sat_df.iloc[:, 0]

    gps_df = gps_df.dropna(subset=["latitude", "longitude"])

    return gps_df


def plot_gps_overlay_map(bridge_df, railjoint_df, turnout_df, gps_df, output_path):
    plt.figure(figsize=(12, 8))

    plt.scatter(
        bridge_df["longitude"],
        bridge_df["latitude"],
        label="Bridge",
        alpha=0.6,
        s=18
    )
    plt.scatter(
        railjoint_df["longitude"],
        railjoint_df["latitude"],
        label="RailJoint",
        alpha=0.6,
        s=18
    )
    plt.scatter(
        turnout_df["longitude"],
        turnout_df["latitude"],
        label="Turnout",
        alpha=0.6,
        s=18
    )

    plt.plot(
        gps_df["longitude"],
        gps_df["latitude"],
        label="Train GPS Route",
        linewidth=1.5,
        alpha=0.9
    )

    plt.scatter(
        gps_df["longitude"],
        gps_df["latitude"],
        alpha=0.4,
        s=8
    )

    plt.title("GPS Route Overlaid on Track Infrastructure")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.legend()
    plt.grid(True)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


def print_basic_summary(bridge_df, railjoint_df, turnout_df, gps_df):
    print("Infrastructure summary:")
    print(f"Bridge points: {len(bridge_df)}")
    print(f"RailJoint points: {len(railjoint_df)}")
    print(f"Turnout points: {len(turnout_df)}")
    print(f"GPS points: {len(gps_df)}")