# netdata_ts_clustering
> Time series clustering for Netdata hosts.


...

## Install

`pip install netdata_ts_clustering`

## Quickstart

```python
model = Clusterer(['london.my-netdata.io'], charts=['system.load'])
model.get_data()
model.df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>system.cpu|guest</th>
      <th>system.cpu|guest_nice</th>
      <th>system.cpu|iowait</th>
      <th>system.cpu|irq</th>
      <th>system.cpu|nice</th>
      <th>system.cpu|softirq</th>
      <th>system.cpu|steal</th>
      <th>system.cpu|system</th>
      <th>system.cpu|user</th>
    </tr>
    <tr>
      <th>time_idx</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1607871202</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.000000</td>
      <td>2.750000</td>
      <td>0.750000</td>
      <td>0.750000</td>
    </tr>
    <tr>
      <th>1607871203</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.247525</td>
      <td>1.980198</td>
      <td>0.990099</td>
      <td>0.742574</td>
    </tr>
    <tr>
      <th>1607871204</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.000000</td>
      <td>0.253165</td>
      <td>1.012658</td>
      <td>0.759494</td>
    </tr>
    <tr>
      <th>1607871205</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.000000</td>
      <td>0.744417</td>
      <td>0.992556</td>
      <td>0.992556</td>
    </tr>
    <tr>
      <th>1607871206</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.248139</td>
      <td>2.481390</td>
      <td>0.496278</td>
      <td>0.744417</td>
    </tr>
  </tbody>
</table>
</div>


