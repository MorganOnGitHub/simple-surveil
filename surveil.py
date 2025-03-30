import argparse
from SurveillanceSystem import SurveillanceSystem

def main():
    parser = argparse.ArgumentParser(description="Real-time object surveillance using YOLO.")

    parser.add_argument("-so","--surveil_object", type=str, default="person", help="The object to detect (default: person).")
    parser.add_argument("-mp","--model_path", type=str, default="models/yolo11l.pt", help="Path to the model file.")
    parser.add_argument("-rd","--record_duration", type=int, default=120, help="Duration of recording in seconds.")
    parser.add_argument("-fs","--frame_skip", type=int, default=5, help="Number of frames to skip (higher values create a time-lapse effect).")

    args = parser.parse_args()

    # Initialize and start surveillance
    surveillance_system = SurveillanceSystem(
        surveil_object=args.surveil_object,
        model_path=args.model_path,
        frame_skip=args.frame_skip,
        record_duration=args.record_duration
    )
    surveillance_system.start_surveillance()

if __name__ == "__main__":
    main()
