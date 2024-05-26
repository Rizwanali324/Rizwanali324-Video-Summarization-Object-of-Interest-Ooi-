

import cv2
from ultralytics import YOLO
import numpy as np
import supervision as sv
import time
import os 
# Define COCO classes and their index mapping
coco_classes = [
    "Person", "Bicycle", "Car", "Motorcycle", "Airplane",
    "Bus", "Train", "Truck", "Boat", "Traffic light",
    "Fire hydrant", "Stop sign", "Parking meter", "Bench",
    "Bird", "Cat", "Dog", "Horse", "Sheep", "Cow",
    "Elephant", "Bear", "Zebra", "Giraffe", "Backpack",
    "Umbrella", "Handbag", "Tie", "Suitcase", "Frisbee",
    "Skis", "Snowboard", "Sports ball", "Kite", "Baseball bat",
    "Baseball glove", "Skateboard", "Surfboard", "Tennis racket", "Bottle",
    "Wine glass", "Cup", "Fork", "Knife", "Spoon",
    "Bowl", "Banana", "Apple", "Sandwich", "Orange",
    "Broccoli", "Carrot", "Hot dog", "Pizza", "Donut",
    "Cake", "Chair", "Couch", "Potted plant", "Bed",
    "Dining table", "Toilet", "TV", "Laptop", "Mouse",
    "Remote", "Keyboard", "Cell phone", "Microwave", "Oven",
    "Toaster", "Sink", "Refrigerator", "Book", "Clock",
    "Vase", "Scissors", "Teddy bear", "Hair drier", "Toothbrush"
]
class_to_index = {cls: idx for idx, cls in enumerate(coco_classes)}

def run_video_summarization(video_path, selected_class_names, update_progress_callback):
    # Ensure the output directory exists
    output_dir = 'processed_video'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_video_path = os.path.join(output_dir, 'output1.mp4')
    model = YOLO('yolov8n.pt')
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Failed to open video source at {video_path}")
        return None, {cls: False for cls in selected_class_names}  # Initialize class_detected dict to False for all classes

    ret, frame = cap.read()
    if not ret:
        print("Failed to get frame from video source")
        cap.release()
        return None, {cls: False for cls in selected_class_names}

    frame_height, frame_width = frame.shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_out = cv2.VideoWriter(output_video_path, fourcc, 20.0, (frame_width, frame_height))

    selected_class_indices = [class_to_index[name] for name in selected_class_names if name in class_to_index]
    class_detected = {cls: False for cls in selected_class_names}  # Track if each class is detected

    tracker = sv.ByteTrack()
    zone_polygon = np.array([[0, 0], [0.5, 0], [0.5, 1], [0, 1]])
    zone_polygon = (zone_polygon * np.array([frame_width, frame_height])).astype(int)
    zone = sv.PolygonZone(polygon=zone_polygon, frame_resolution_wh=(frame_width, frame_height))
    zone_annotator = sv.PolygonZoneAnnotator(zone=zone, color=sv.Color.RED, thickness=2, text_thickness=4, text_scale=2)
    bounding_box_annotator = sv.BoundingBoxAnnotator()
    label_annotator = sv.LabelAnnotator()
    trace_annotator = sv.TraceAnnotator()

    frame_count = 0
    start_time = time.time()

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        results = model(frame)
        detections = sv.Detections.from_ultralytics(results[0])
        detections = detections[np.isin(detections.class_id, selected_class_indices)]
        detections = tracker.update_with_detections(detections)

        for class_id in detections.class_id:
            class_name = model.model.names[class_id]
            if class_name in class_detected:
                class_detected[class_name] = True

        zone_triggered_detections = zone.trigger(detections=detections)
        if zone_triggered_detections.any():
            annotated_frame = bounding_box_annotator.annotate(scene=frame, detections=detections)
            labels = [f"#{tracker_id} {model.model.names[class_id]} ({conf:.2f})" for class_id, tracker_id, conf in zip(detections.class_id, detections.tracker_id, detections.confidence)]
            annotated_frame = label_annotator.annotate(scene=annotated_frame, detections=detections, labels=labels)
            annotated_frame = trace_annotator.annotate(scene=annotated_frame, detections=detections)
            annotated_frame = zone_annotator.annotate(scene=annotated_frame)
            video_out.write(annotated_frame)

        frame_count += 1
        if frame_count % 10 == 0:
            progress = int((frame_count / cap.get(cv2.CAP_PROP_FRAME_COUNT)) * 100)
            update_progress_callback(progress)

    cap.release()
    video_out.release()
    cv2.destroyAllWindows()
    print(f"Output video has been saved to {output_video_path}")
    return output_video_path, class_detected
