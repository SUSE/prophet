FROM opensuse/leap

RUN zypper --non-interactive up && \
    zypper --non-interactive install git ruby-devel make gcc gcc-c++ build wget curl vim

RUN gem install bundler -v 1.17.3

RUN mkdir /prophet ~/.ssh && \
    ssh-keyscan github.com > ~/.ssh/known_hosts
WORKDIR /prophet
COPY . /prophet

RUN gem build prophet.gemspec && \
    gem install prophet*.gem && \
    bundle.ruby2.5 install

CMD ["ruby", "prophet/prophet.rb"]
