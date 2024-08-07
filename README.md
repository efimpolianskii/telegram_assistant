# Notes
In the current repository I have gained all the python scripts integrated with telegram API to help me as a personal assistant with some basic staff, on which I spend too much valuable time. 
## Environment
To run the scripts I use Jupyter dokcer container with jupyter-scheduler plugin on my VPS. To tell the truth, there are so many ways to realize scheduled tasks/scripts, but I have chosen this method as the most convenient, fast and simple.
1. As a VPS provider, I have chosen [Hostinger](https://www.hostinger.com/vps-hosting) as one of the cheapest and user-friendly provider. At the moment the monthly subscription costs arounf $5. So, not so terrible, especially for those, who know how to spend VPS resources wisely.
2. This is the docker container I used - [jupyter/datascience-notebook](https://hub.docker.com/r/jupyter/datascience-notebook). I set it up for my work, however, in personal life it became even more useful.
3. If you are going to choose the same method of telegram alerts bot hosting, don't forget about restart policy while running the container
   - `docker run -d --restart unless-stopped -p 8080:8888 jupyter/datascience-notebook`,
   - and also check the docker container logs to copy the jupyter token (you won't be able to enter the gui on the 8080 port) - `docker logs <container_id>`.
5. Then I did some staff insedi the jupyter container (again, these steps are only for those who, as myself, have chosen this way of running alerts):
   - navigate inside the container `docker exec -it <container_id_or_name> bash`,
   - install jupyter-scheduler plugin `pip install jupyter-scheduler`,
   - enable it `jupyter server extension enable jupyter_scheduler`,
   - restart the container `docker restart <container_id_or_name>`.
