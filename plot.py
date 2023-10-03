import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys

df = pd.read_json(sys.argv[1], lines=True)
blocks = df.groupby('msg').get_group("Validating incoming gossip block message").dropna(axis=1, how='all').apply(lambda y: y.apply(lambda x: x['value'] if type(x) == dict else x))

ax = sns.histplot(blocks, x='decompressed', log_scale=(False,True))
ax.set(xlabel='block size (uncompressed) [bytes]',
       ylabel='occurances',
       title='Block size distribution')
plt.show()

blocks['compratio'] = blocks['decompressed']/blocks['len']
ax = sns.scatterplot(blocks, x='decompressed', y='compratio').set(xscale="log")
plt.xlabel('block size (uncompressed) [bytes]')
plt.ylabel('compression ratio')
plt.title('Block compression')
plt.show()

ax = sns.scatterplot(blocks, x='len', y='receiveDelay').set(yscale="log", xscale="log")
plt.xlabel('block size (compressed) [bytes]')
plt.ylabel('Reception Delay [ns]')
plt.title('Block reception delay for different sized blocks')
plt.show()

ax = sns.displot(blocks, kind="ecdf", x="receiveDelay").set(xscale="log")
plt.ylabel('CDF: portion of blocks received before given delay')
plt.xlabel('Reception Delay [ns]')
plt.title('CDF: Block reception delay')
plt.show()
