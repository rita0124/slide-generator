FROM amancevice/pandas

ENV TZ=Asia/Taipei
RUN apt-get update -y
RUN apt-get install xfonts-utils -y
RUN wget https://www.twfont.com/chinese/font/TaipeiSans.ttf
RUN cp *.ttf /usr/share/fonts/truetype && cd /usr/share/fonts/truetype
RUN mkfontscale && mkfontdir && fc-cache

WORKDIR /source_code
RUN mkdir pics libs ppt
COPY requirements.txt config.ini main.py /source_code
COPY ./libs /source_code/libs/
COPY ./ppt /source_code/ppt/
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
