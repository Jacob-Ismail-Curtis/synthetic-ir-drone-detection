# Dissertation Project
I undertook this dissertation in my final year studying BSc Computer Science at Durham University. The focus of the project was to investigate the generation of synthetic infrared drone imagery for the purpose of improving detection for Counter-UAV Systems. This repository contains the [final report](https://github.com/Jacob-Ismail-Curtis/synthetic-ir-drone-detection/final_report.pdf) based on my investigations and experiments.

## Abstract

This paper presents a novel approach for enhancing infrared (IR) drone detection using synthetic IR drone imagery. The proposed approach involves creating a diverse, synthetic dataset which is used to augment a training dataset for a YOLOv7 model, capable of detecting drones in real-time. The paper introduces two data augmentation techniques for generating IR drone imagery. The first technique involves rendering 3D drones in Blender by randomising simulation parameters, applying post-processing and pasting them onto a 2D IR scene, while the second technique uses an adversarial data augmentation methodology to reduce the synthetic-real domain gap for these 3D drone renders. The proposed approach addresses the challenge of limited IR drone imagery for training and offers promising results for improving drone monitoring systems for counter-UAV applications. The model shows an average of 93.8% accuracy when training data is augmented by 20% using synthetic data, which is an 2.8% improvement on the model trained using only ‘real’ drone dataset.

## Code Provided

The code provided is what I have remaining of the project on my laptop. The full system is on Durham University's NCC server which I no longer have access to. I have provided the Python code to be used in Blender to generate synthetic IR drone imagery from a drone.obj model. This model can be found [here](https://drive.google.com/file/d/1t5RMzuu3sSSjUmxmp90Zp_ISA9OMtjHU/view?usp=drive_link). I have also provided code to preprocess the synthetic images to pass through the CycleGAN, the train and test files for the CycleGAN and a Jupyter notebook to run it. Code is provided only as a reference and requires rebuilding to be able to use the full system.

## Future Work

Future work based on the dissertation conclusion includes exploring drone classification by developing a dataset specifically designed for this purpose, examining the performance of two-stage detectors like Faster R-CNN for drone detection, expanding the research to include other drone model types such as fixed-wing drones and exploring the detection of other flying objects like helicopters and planes. Additionally, conducting an ablation study to quantify the effects of individual post-processing techniques used for synthetic data generation, validating the effectiveness of synthetic IR training data on unseen datasets, and integrating the drone detection system into a comprehensive monitoring system by merging it with a generic object tracker are suggested avenues for further research.

## Feedback
The final mark received for the whole project was **76%** (high first class).

> By [Jacob-Ismail-Curtis](https://github.com/Jacob-Ismail-Curtis).
