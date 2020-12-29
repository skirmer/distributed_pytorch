import s3fs
import dask


s3 = s3fs.S3FileSystem(anon=True)
from PIL import Image


from IPython.display import display, HTML
gpu_links = f'''
<b>Cluster Dashboard links</b>
<ul>
<li><a href="{client.dashboard_link}/status" target="_blank">CPU dashboard</a></li>
<li><a href="{client.dashboard_link}/individual-gpu-utilization" target="_blank">GPU utilization</a></li>
<li><a href="{client.dashboard_link}/individual-gpu-memory" target="_blank">GPU memory</a></li>
</ul>
'''

@dask.delayed
def reformat(batch):
    flat_list = [item for item in batch]
    tensors = [x[1] for x in flat_list]
    names = [x[0] for x in flat_list]
    labels = [x[2] for x in flat_list]
    
    tensors = torch.stack(tensors).to(device)
    
    return [names, tensors, labels]
