 Video-Summarization-Object-of-Interest

## Objective
The aim of this project is to develop a deep learning-based video summarization framework that allows users to efficiently summarize large volumes of surveillance video data, focusing specifically on predefined Objects of Interest (OoI) such as persons, airplanes, mobile phones, bikes, and cars. This system is designed to streamline the process of reviewing video content from surveillance footage, crucial for enhancing security measures and operational efficiency in both public and private sectors.

## Background
With the proliferation of digital video technology, surveillance systems have become ubiquitous in security and safety operations across various industries. These systems generate a substantial amount of video data daily, presenting challenges in storage, processing, and analysis. Traditional methods of video analysis are not only time-consuming but also require substantial computational resources, making them inefficient for real-time applications.

## Solution: Deep Learning-Based Video Summarization
The proposed framework leverages advanced deep learning algorithms to automatically detect and prioritize video segments that contain specified Objects of Interest. This approach significantly reduces the volume of data to be reviewed manually, thereby saving time and computational resources while maintaining the effectiveness of the surveillance system.
## Proposed Architecture of the Algorithm

The following diagram illustrates the architecture of the proposed framework for video summarization. This architecture is designed to utilize deep learning techniques for efficient object detection and summarization in surveillance videos.

![Proposed Architecture](![Alt text](GUI/Architecture-of-the-proposed-framework.png))

This architecture is centered around the use of advanced object detection models and summarization algorithms to process and reduce large volumes of video data into concise segments that highlight critical Objects of Interest (OoI).

# GUI

<p align="center">
  <img src="GUI/Gui1.PNG" alt="GUI 1" style="width: 45%;">
  <img src="GUI/Gui2.PNG" alt="GUI 2" style="width: 45%;">
</p>

## Video Comparison

original video and the output summarized video side by side for comparison:

<p align="center">
<video src="Results_Videos/test1_output.mp4" controls title="Title"></video>  
</p>


## Technologies Used

<p align="left">
  <a href="https://opencv.org/" target="_blank" rel="noreferrer">
    <img src="https://www.vectorlogo.zone/logos/opencv/opencv-icon.svg" alt="opencv" width="50" height="50"/>
  </a>
  <a href="https://www.python.org" target="_blank" rel="noreferrer">
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="50" height="50"/>
  </a>
  <a href="https://pytorch.org/" target="_blank" rel="noreferrer">
    <img src="https://www.vectorlogo.zone/logos/pytorch/pytorch-icon.svg" alt="pytorch" width="50" height="50"/>
  </a>
  <a href="https://www.tensorflow.org" target="_blank" rel="noreferrer">
    <img src="https://www.vectorlogo.zone/logos/tensorflow/tensorflow-icon.svg" alt="tensorflow" width="50" height="50"/>
  </a>
  <a href="https://keras.io/" target="_blank" rel="noreferrer">
    <img src="https://keras.io/img/logo.png" alt="keras" width="50" height="50"/>
  </a>
  <a href="https://numpy.org/" target="_blank" rel="noreferrer">
    <img src="https://numpy.org/images/logo.svg" alt="numpy" width="50" height="50"/>
  </a>
  <a href="https://pandas.pydata.org/" target="_blank" rel="noreferrer">
    <img src="https://raw.githubusercontent.com/devicons/devicon/2ae2a900d2f041da66e950e4d48052658d850630/icons/pandas/pandas-original.svg" alt="pandas" width="50" height="50"/>
  </a>
  <a href="https://scikit-learn.org/" target="_blank" rel="noreferrer">
    <img src="https://upload.wikimedia.org/wikipedia/commons/0/05/Scikit_learn_logo_small.svg" alt="scikit_learn" width="50" height="50"/>
  </a>
  <a href="https://colab.research.google.com/" target="_blank" rel="noreferrer">
    <img src="https://colab.research.google.com/img/colab_favicon_256px.png" alt="colab" width="50" height="50"/>
  </a>
  <a href="https://roboflow.com/" target="_blank" rel="noreferrer">
    <img src="https://app.roboflow.com/images/logomark-color.svg" alt="roboflow" width="50" height="50"/>
  </a>
  <a href="https://ultralytics.com/" target="_blank" rel="noreferrer">
    <img src="https://github.com/ultralytics/assets/raw/main/logo/Ultralytics_Logotype_Reverse.svg" alt="ultralytics" width="50" height="50"/>
  </a>
</p>

## Key Features
- **Object of Interest Identification**: Utilizes state-of-the-art object recognition models to accurately identify and classify key objects in the video footage as specified by the user (e.g., person, airplane).
- **Customizable Summaries**: Allows users to customize the summary output based on specific objects of interest, enhancing the relevance of the summarized content to particular security or operational needs.
- **Efficiency and Scalability**: Designed to handle large volumes of video data efficiently, making it suitable for both small-scale and large-scale surveillance systems.
- **User-Friendly Interface**: Provides an intuitive interface for users to specify their preferences for summarization, making the system accessible to personnel without technical expertise.

## Implementation Strategy
1. **Data Collection**: Collect and annotate a diverse dataset of video clips containing the targeted objects of interest.
2. **Model Training**: Train deep learning models on the annotated dataset to develop robust object recognition capabilities.
3. **Summarization Algorithm**: Develop an algorithm that extracts and compiles video segments featuring the identified objects into a concise summary.
4. **Testing and Validation**: Test the framework with real-world surveillance footage to validate effectiveness, accuracy, and efficiency.

## Limitations
- **Dependency on Quality of Input Data**: The accuracy of object detection and summarization is highly dependent on the quality and resolution of the input video, which can vary significantly in real-world surveillance setups.
- **Processing Time**: Despite optimizations, processing high-resolution videos or large volumes of data can still be time-consuming and resource-intensive.
