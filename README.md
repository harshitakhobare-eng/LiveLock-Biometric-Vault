🛡️ LiveLock: Privacy-First Biometric Vault

LiveLock is a privacy-focused biometric authentication system that replaces traditional passwords with encrypted facial embeddings and real-time liveness verification.
Instead of storing raw facial images, LiveLock extracts a 128-dimensional face embedding and encrypts it before storage. This ensures that even if the database is compromised, sensitive biometric data remains protected.
The project was built to explore how AI-based authentication systems can be secure, practical, and privacy-preserving at the same time.

Why LiveLock?
Most biometric systems store raw facial images, which creates a major privacy risk. Once biometric data is leaked, it cannot be changed like a password.
LiveLock was designed with three core goals:
1. Zero image storage
2. Encrypted biometric data
3. Real-time anti-spoofing protection
This project demonstrates how face recognition can be implemented responsibly.

Features:
1. 128D facial embedding extraction using a ResNet-based model
2. Encrypted embedding storage using Fernet symmetric encryption
3. Salted biometric data for additional security
4. Real-time liveness detection (blink + head movement challenges)
5. Euclidean distance-based identity verification
6. Interactive Streamlit dashboard for enrollment and login

How It Works:
A face is captured using OpenCV.
A 128-dimensional embedding is generated.
The embedding is salted and encrypted.
Encrypted data is stored in an SQLite database.
During login, liveness challenges are performed.
A new embedding is generated and compared using:
                                                 
                                                 d = sqrt(sum((xi - yi)^2)) for i = 1 to 128

If the similarity threshold is satisfied, access is granted.

Tech Stack:
Python
OpenCV
face-recognition
dlib
NumPy
SciPy
SQLite
cryptography (Fernet)
Streamlit

Installation--
Clone the repository:
git clone https://github.com/yourusername/LiveLock-Biometric-Vault.git
cd LiveLock-Biometric-Vault

Install dependencies:
pip install streamlit face-recognition opencv-python numpy cryptography scipy

Run the application:
streamlit run dashboard.py

Security Approach:
1. No raw facial images are stored
2. Only encrypted embeddings are saved
3. Salt is applied before encryption
4. Liveness detection prevents photo spoofing attacks
5. Threshold tuning balances security and usability

Challenges Faced:
1. Calibrating similarity thresholds for accurate authentication
2. Handling real-time webcam inconsistencies
3. Debugging subprocess communication with Streamlit
4. Managing security without compromising usability

What This Project Represents:
LiveLock is more than a face recognition demo. It is an attempt to combine AI, security, and ethical design into a single system.
This project strengthened my understanding of:
1. High-dimensional vector similarity
2. Real-time computer vision
3. Encryption and secure storage
4. System-level architecture and debugging

Future Improvements:
1. Cosine similarity implementation
2. Deep learning–based anti-spoofing models
3. Multi-factor authentication
4. Scalable deployment architecture

👩‍💻 Author

Harshita Khobare
Computer Science Engineering Student
