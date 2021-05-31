import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


def get_data(data_filename):
    dat = pd.read_csv(data_filename, sep=' ', names=['TimeStamps', 'Operation', 'QueueLength'])
    return dat

def plot_queue_length_for_each_time_stamps(dat, arrival_rate):
    plt.figure(figsize=(20,8))
    plt.plot(dat['TimeStamps'], dat['QueueLength'], '-',
            color='gray',
            markersize=8, linewidth=2,
            markerfacecolor='white',
            markeredgewidth=2)
    plt.ylabel('Queue Length (packets)')
    plt.xlabel('Timestamps (s)')
    plt.title('Lambda = {arrival_rate}')
    plt.savefig('QueueLength_{arrival_rate}.png')

def get_average_queue_length(dat):
    total_length = np.sum(dat['QueueLength'])
    return total_length / len(dat)

def get_average_drop_rate(dat):
    num_drop = np.sum(dat[dat['Operation']=='d']['QueueLength'])
    return num_drop / len(dat)

def get_average_response_time(dat):
    #Record timestamps in which a dequeue occurs
    dequeue_tmp = dat[dat['Operation'] == '-']['TimeStamps']
    #Calculate response time between each dequeue event(response time)
    res_time = (dequeue_tmp - dequeue_tmp.shift(1)).dropna()
    return np.sum(res_time) / len(res_time)


results = {'AVG_QUEUE_LENGTH': [],
           'AVG_DROP_RATE': [],
           'AVG_RESP_TIME': []
           }

#Modify your own lambdas here (must be smaller than mu)
arrival_rates = [13, 14, 15, 17, 18]
for arrival_rate in arrival_rates:
    #Create data with respect to lambda
    os.system(f'sudo python3 ./waf --run "mm1-queue --queueLimit=40 --lambda={arrival_rate} --mu=20"')
    #Save data file in to pandas data frame
    data = get_data(f'mm1queue_lambda_{arrival_rate}.dat')
    #Get necessary information for each data frame
    results['AVG_QUEUE_LENGTH'].append(get_average_queue_length(data))
    results['AVG_DROP_RATE'].append(get_average_drop_rate(data))
    results['AVG_RESP_TIME'].append(get_average_response_time(data))
    #I need help with calculate average idle rate
    #Generate queue length plots wrt each lambda
    plot_queue_length_for_each_time_stamps(data, arrival_rate)

#Generate plots of avg_queuelength, avg_droprate as a function of lambda
plt.figure(0,figsize=(16,9))
plt.plot(arrival_rates, results['AVG_QUEUE_LENGTH'], '-')
plt.ylabel('AVG Queue Length')
plt.xlabel('Lambda')
plt.savefig('AVG_queue_length.png')


plt.figure(figsize=(16,9))
plt.plot(arrival_rates, results['AVG_DROP_RATE'], '-')
plt.ylabel('AVG Drop Rate')
plt.xlabel('Lambda')
plt.savefig('AVG_drop_rate.png')

plt.figure(figsize=(16,9))
plt.plot(arrival_rates, results['AVG_RESP_TIME'], '-')
plt.ylabel('AVG Response Time')
plt.xlabel('Lambda')
plt.savefig('AVG_resp_time.png')
