import pickle
import numpy as np
import matplotlib.pyplot as plt

from rand_seq import CircuitDataPoint

with open( "native3_8.dat", 'rb' ) as f:
    data3 = pickle.load( f )

with open( "native4_16.dat", 'rb' ) as f:
    data4 = pickle.load( f )

X3 = list( range( len( data3 ) ) )
Y3_qs_time = []
Y3_qf_time = []
Y3_qs_avg_time = []
Y3_qf_avg_time = []
Y3_qs_num = []
Y3_qf_num = []

for pt in data3:
    Y3_qs_num.append( pt.data[ "qsearch_retries" ] )
    Y3_qf_num.append( pt.data[ "qfactor_retries" ] )

    Y3_qs_time.append( sum( pt.data[ "qsearch_retry_times" ] ) )
    Y3_qf_time.append( sum( pt.data[ "qfactor_retry_times" ] ) )

    Y3_qs_avg_time.append( sum( pt.data[ "qsearch_retry_times" ] ) / len( X3 ) )
    Y3_qf_avg_time.append( sum( pt.data[ "qfactor_retry_times" ] ) / len( X3 ) )

X4 = list( range( len( data4 ) ) )
Y4_qs_time = []
Y4_qf_time = []
Y4_qs_avg_time = []
Y4_qf_avg_time = []
Y4_qs_num = []
Y4_qf_num = []

for pt in data4:
    Y4_qs_num.append( pt.data[ "qsearch_retries" ] )
    Y4_qf_num.append( pt.data[ "qfactor_retries" ] )

    Y4_qs_time.append( sum( pt.data[ "qsearch_retry_times" ] ) )
    Y4_qf_time.append( sum( pt.data[ "qfactor_retry_times" ] ) )

    Y4_qs_avg_time.append( sum( pt.data[ "qsearch_retry_times" ] ) / len( X3 ) )
    Y4_qf_avg_time.append( sum( pt.data[ "qfactor_retry_times" ] ) / len( X3 ) )

# 3-Qubit
fig, ax = plt.subplots( 1, 1, dpi = 600 )
bins = np.linspace( 0, 90, 100 )
ax.set_title( "Total Time to Solution on Random 3-Qubit Circuits" )
ax.set_xlabel( "Seconds" )
ax.set_ylabel( "Number of Circuits" )
ax.hist( Y3_qs_time, bins, label = "Qsearch", alpha = 0.5 )
ax.hist( Y3_qf_time, bins, label = "Qfactor", alpha = 0.5 )
ax.legend()
fig.savefig( "native3q.png" )

# 4-Qubit
fig, ax = plt.subplots( 1, 1, dpi = 600 )
bins = np.linspace( 0, 360, 100 )
ax.set_title( "Total Time to Solution on Random 4-Qubit Circuits" )
ax.set_xlabel( "Seconds" )
ax.set_ylabel( "Number of Circuits" )
ax.hist( Y4_qs_time, bins, label = "Qsearch", alpha = 0.5 )
ax.hist( Y4_qf_time, bins, label = "Qfactor", alpha = 0.5 )
ax.legend()
fig.savefig( "native4q.png" )
