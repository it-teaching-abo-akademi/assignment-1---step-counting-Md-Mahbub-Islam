import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

#Simple function to visualize 4 arrays that are given to it
def visualize_data(timestamps, x_arr,y_arr,z_arr,s_arr):
  #Plotting accelerometer readings
  plt.figure(1)
  plt.plot(timestamps, x_arr, color = "blue",linewidth=1.0)
  plt.plot(timestamps, y_arr, color = "red",linewidth=1.0)
  plt.plot(timestamps, z_arr, color = "green",linewidth=1.0)
  plt.show()
  #magnitude array calculation
  m_arr = []
  for i, x in enumerate(x_arr):
    m_arr.append(magnitude(x_arr[i],y_arr[i],z_arr[i]))
  plt.figure(2)
  #plotting magnitude and steps
  plt.plot(timestamps, s_arr, color = "black",linewidth=1.0)
  plt.plot(timestamps, m_arr, color = "red",linewidth=1.0)
  #give label to x and y axis
  plt.xlabel("Time Steps")
  plt.ylabel("Acceleration Magnitude")
  plt.show()

#Function to read the data from the log file
def read_data(filename):
  timestamps = []
  x_array = []
  y_array = []
  z_array = []
  with open(filename) as f:
      for line in f:
          data = line.split(',')
          timestamps.append(int(data[0]))
          x_array.append(float(data[1]))
          y_array.append(float(data[2]))
          z_array.append(float(data[3]))

  return timestamps, x_array, y_array, z_array


#Function to count steps.
#Should return an array of timestamps from when steps were detected
#Each value in this array should represent the time that step was made.
def count_steps(timestamps, x_arr, y_arr, z_arr):
  #magnitude array calculation
  m_arr = []
  for i, x in enumerate(x_arr):
    m_arr.append(magnitude(x_arr[i],y_arr[i],z_arr[i]))


  #find mean of magnitude array
  mean = int(np.mean(m_arr)) # Whole number
  print(mean)
  threshold = mean * 2

  #step array calculation
  s_t = []
  for i, x in enumerate(m_arr):
      if m_arr[i] > threshold and m_arr[i-1] < threshold: #if current value is greater than mean and previous value is less than mean
          s_t.append(timestamps[i])

  #plot a line at threshold
  plt.figure(2)
  plt.plot(timestamps, m_arr, color="red", linewidth=1.0)
  plt.axhline(y=threshold, color='b', linestyle='-', label="Threshold")
  plt.xlabel("Time Steps")
  plt.ylabel("Acceleration Magnitude")
  plt.show()

  return s_t


#Calculate the magnitude of the given vector
def magnitude(x,y,z):
  return np.linalg.norm((x,y,z)) #np.sqrt(x*x+y*y+z*z)

#Function to convert array of times where steps happened into array to give into graph visualization
#Takes timestamp-array and array of times that step was detected as an input
#Returns an array where each entry is either zero if corresponding timestamp has no step detected or 50000 if the step was detected
def generate_step_array(timestamps, step_time):
  s_arr = []
  ctr = 0
  for i, time in enumerate(timestamps):
    if(ctr<len(step_time) and step_time[ctr]<=time):
      ctr += 1
      s_arr.append( 60 ) # in my case magnitude is so small that 50000 is too big
    else:
      s_arr.append( 0 )
  while(len(s_arr)<len(timestamps)):
    s_arr.append(0)
  return s_arr

#Check that the sizes of arrays match
def check_data(t,x,y,z):
  if( len(t)!=len(x) or len(y)!=len(z) or len(x)!=len(y) ):
    print("Arrays of incorrect length")
    return False
  print("The amount of data read from accelerometer is "+str(len(t))+" entries")
  return True

#helps to visualize initial data
def plot_raw_data(timestamps, x_array, y_array, z_array):
  plt.figure(1)
  plt.plot(timestamps, x_array, color="blue", linewidth=1.0)
  plt.plot(timestamps, y_array, color="red", linewidth=1.0)
  plt.plot(timestamps, z_array, color="green", linewidth=1.0)
  #give label to x and y axis
  plt.xlabel("Time Steps")
  plt.ylabel("Acceleration")

  plt.show()

def advanced_step_counter(timestamps, x_array, y_array, z_array):
  print("Advanced step counter")

  #magnitude array calculation
  m_arr = []
  for i, x in enumerate(x_array):
      m_arr.append(magnitude(x_array[i],y_array[i],z_array[i]))

  #plot magnitude array
  plt.figure(2)
  plt.plot(timestamps, m_arr, color="red", linewidth=1.0)
  plt.xlabel("Time Steps")
  plt.ylabel("Acceleration Magnitude")
  plt.show()



  #low pass filter
  b, a = signal.butter(3, 0.05, 'low', analog=False)
  x_array = signal.filtfilt(b, a, x_array)
  y_array = signal.filtfilt(b, a, y_array)
  z_array = signal.filtfilt(b, a, z_array)

  #magnitude array calculation
  m_arr = []
  for i, x in enumerate(x_array):
      m_arr.append(magnitude(x_array[i], y_array[i], z_array[i]))

  #remove gravity from magnitude array at 9.8
  for i, x in enumerate(m_arr):
      m_arr[i] = m_arr[i] - 9.8


  #plot magnitude
  plt.figure(2)
  plt.plot(timestamps, m_arr, color="red", linewidth=1.0)
  plt.xlabel("Time Steps")
  plt.ylabel("Acceleration Magnitude")
  plt.show()

  #find peaks of magnitude above certain threshold

  peaks, _ = signal.find_peaks(m_arr, height=1)
  print(peaks)
  #convert to numpy array
  peaks = np.asarray(peaks)
  timestamps = np.asarray(timestamps)
  m_arr = np.asarray(m_arr)

  print(f"Total number of peaks: {len(peaks)}")

  #plot peaks
  plt.figure(2)
  plt.plot(timestamps, m_arr)
  plt.plot(timestamps[peaks], m_arr[peaks], "x")
  plt.xlabel("Time Steps")
  plt.ylabel("Acceleration Magnitude")
  plt.show()


def main():
  #read data from a measurement file, change the inoput file name if needed
  # timestamps, x_array, y_array, z_array = read_data("walk1.csv")
  timestamps, x_array, y_array, z_array = read_data("slow_fast_jump.csv")


  #plot timestamps, x_array, y_array, z_array
  plot_raw_data(timestamps, x_array, y_array, z_array)

  #Chek that the data does not produce errors
  if(not check_data(timestamps, x_array,y_array,z_array)):
    return


  st = advanced_step_counter(timestamps, x_array, y_array, z_array)
  # #Count the steps based on array of measurements from accelerometer
  # st = count_steps(timestamps, x_array, y_array, z_array)
  # #Print the result
  # print("This data contains "+str(len(st))+" steps according to current algorithm")
  # # #convert array of step times into graph-compatible format
  # s_array = generate_step_array(timestamps, st)
  #
  # # #visualize data and steps
  # visualize_data(timestamps, x_array,y_array,z_array,s_array)

main()

