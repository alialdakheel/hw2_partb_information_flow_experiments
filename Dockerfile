FROM krallin/ubuntu-tini:bionic

SHELL ["/bin/bash", "-c"]

# Update ubuntu and setup conda
# adapted from: https://hub.docker.com/r/conda/miniconda3/dockerfile
RUN sed -i'' 's/archive\.ubuntu\.com/us\.archive\.ubuntu\.com/' /etc/apt/sources.list
RUN apt-get clean -qq \
    && rm -r /var/lib/apt/lists/* -vf \
    && apt-get clean -qq \
    && apt-get update -qq \
    && apt-get upgrade -qq \
    # git and make for `npm install`, wget for `install-miniconda`
    && apt-get install wget git make unzip vim nano -qq \
    # deps to run firefox inc. with xvfb
    && apt-get install libgtk-3-0 libx11-xcb1 libdbus-glib-1-2 libxt6 xvfb -qq

RUN wget https://github.com/mozilla/OpenWPM/archive/v0.12.0.zip
RUN unzip v0.12.0.zip

ENV HOME /opt
RUN cp OpenWPM-0.12.0/scripts/install-miniconda.sh .
RUN cp -r OpenWPM-0.12.0 /opt/OpenWPM
RUN ./install-miniconda.sh
ENV PATH $HOME/miniconda/bin:$PATH

# Install OpenWPM
WORKDIR /opt/OpenWPM
RUN git clone https://github.com/tadatitam/info-flow-experiments.git adfisher
RUN mkdir logs
RUN rm environment.yaml
RUN wget https://raw.githubusercontent.com/alialdakheel/hw2_partb_information_flow_experiments/master/OpenWPM-0.12.0/environment.yaml
RUN wget https://raw.githubusercontent.com/alialdakheel/hw2_partb_information_flow_experiments/master/news_demo.py
RUN wget https://raw.githubusercontent.com/alialdakheel/hw2_partb_information_flow_experiments/master/google_click_search_demo.py
RUN wget https://raw.githubusercontent.com/alialdakheel/hw2_partb_information_flow_experiments/master/google_search_demo.py
RUN wget https://raw.githubusercontent.com/alialdakheel/hw2_partb_information_flow_experiments/master/helpers.py
RUN wget https://raw.githubusercontent.com/alialdakheel/hw2_partb_information_flow_experiments/master/news.py
RUN wget https://raw.githubusercontent.com/alialdakheel/hw2_partb_information_flow_experiments/master/ml.py
RUN wget https://raw.githubusercontent.com/alialdakheel/hw2_partb_information_flow_experiments/master/ml_test.py
RUN wget https://raw.githubusercontent.com/alialdakheel/hw2_partb_information_flow_experiments/master/permutation_test.py
RUN wget https://raw.githubusercontent.com/alialdakheel/hw2_partb_information_flow_experiments/master/statistics.py
RUN wget https://raw.githubusercontent.com/alialdakheel/hw2_partb_information_flow_experiments/master/queries.txt
RUN wget https://raw.githubusercontent.com/alialdakheel/hw2_partb_information_flow_experiments/master/sites.txt
COPY hw2.py .
RUN ./install.sh
ENV PATH $HOME/miniconda/envs/openwpm/bin:$PATH

# Move the firefox binary away from the /opt/OpenWPM root so that it is available if
# we mount a local source code directory as /opt/OpenWPM
RUN mv firefox-bin /opt/firefox-bin
ENV FIREFOX_BINARY /opt/firefox-bin/firefox-bin

# Setting demo.py as the default command
#CMD [ "python", "demo.py"]
CMD ["bash"]
