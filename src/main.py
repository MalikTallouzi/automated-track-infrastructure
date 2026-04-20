from pathlib import Path
from mapping import (
    load_infrastructure_data,
    plot_infrastructure_map,
    load_gps_data,
    plot_gps_overlay_map,
    print_basic_summary,
)


def main():
    
    bridge_path = "data1/converted_coordinates_Resultat_Bridge.csv"
    railjoint_path = "data1/converted_coordinates_Resultat_RailJoint.csv"
    turnout_path = "data1/converted_coordinates_Turnout.csv"

    run_folder = Path("data2/run1")

    latitude_path = run_folder / "GPS.latitude.csv"
    longitude_path = run_folder / "GPS.longitude.csv"
    speed_path = run_folder / "GPS.speed.csv"
    satellites_path = run_folder / "GPS.satellites.csv"

    output_folder = Path("output")
    infrastructure_output = output_folder / "infrastructure_map.png"
    overlay_output = output_folder / "gps_overlay_map.png"

    print("Loading infrastructure data...")
    bridge_df, railjoint_df, turnout_df = load_infrastructure_data(
        bridge_path,
        railjoint_path,
        turnout_path
    )

    print("Saving infrastructure map...")
    plot_infrastructure_map(
        bridge_df,
        railjoint_df,
        turnout_df,
        infrastructure_output
    )

    print("Loading GPS data...")
    gps_df = load_gps_data(
        latitude_path=latitude_path,
        longitude_path=longitude_path,
        speed_path=speed_path,
        satellites_path=satellites_path
    )

    print("Saving GPS overlay map...")
    plot_gps_overlay_map(
        bridge_df,
        railjoint_df,
        turnout_df,
        gps_df,
        overlay_output
    )

    print_basic_summary(bridge_df, railjoint_df, turnout_df, gps_df)

    print("\nDone.")
    print(f"Infrastructure map saved to: {infrastructure_output}")
    print(f"GPS overlay map saved to: {overlay_output}")


if __name__ == "__main__":
    main()