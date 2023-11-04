# RaspberryPi-car
Building a Raspberry Pi car involves various steps, from assembling it to testing and adding remote control features.

### Current Progress
- [x] Car assembly
- [x] System tests
- [x] Car controller
- [x] UI for car controller
- [ ] Improve controller style
- [x] Switch to Flask server

## Getting started
1. Clone repository to Raspberry Pi and your computer
   ```python
   git clone https://github.com/KyloRen1/RaspberryPi-car
   ```
2. Create python environment in Raspberry Pi and your computer
   ```python
    python3 -m venv venv 
    source venv/bin/activate
    pip install -r requirements.txt
   ```
3. Run test on Raspberry Pi
   ```python
    pytest
   ```

4. Launch video stream on Raspberry Pi
   ```python
   cd RaspberryPi-car/src/car/mjpg-streamer/
   make USE_LIBV4L2=true clean all
   sh start_streamer.sh
   ```

5. Launch server on Raspberry Pi
   ```python
   python -m src.car.main
   ```

6. Laucnh client on your computer
   ```python
   python src/client/view.py
   ```

## System checks
Testing of the system for buzzer, ligths, wheels and turns, using pytest.

<div style="display:block;margin-top: 15px; margin-bottom: 30px" align="center">
    <img src="assets/car.gif" alt="GIF 1" width="30%">
    <img src="assets/test.gif" alt="GIF 2" width="53%">
</div>
