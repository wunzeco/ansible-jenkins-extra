require 'spec_helper'

jenkins_extra_home = "/var/lib/jenkins"

describe file("#{jenkins_extra_home}/.aws/credentials") do
  it { should be_file }
  it { should be_mode 600 }
end

describe file("#{jenkins_extra_home}/.aws/config") do
  it { should be_file }
  it { should be_mode 600 }
end

describe file("#{jenkins_extra_home}/create-credentials-config.py") do
  it { should be_file }
  it { should be_mode 755 }
end

describe file("#{jenkins_extra_home}/.ssh/infra-myawesomekey") do
  it { should be_file }
  it { should be_mode 600 }
end

describe file("#{jenkins_extra_home}/.ssh/infra-myawesomekey.pub") do
  it { should be_file }
  it { should be_mode 644 }
end

describe file("#{jenkins_extra_home}/.ssh/infra-anotherkey.pem") do
  it { should be_file }
  it { should be_mode 600 }
end

describe file("#{jenkins_extra_home}/.ssh/infra-anotherkey.pub") do
  it { should be_file }
  it { should be_mode 644 }
end

describe file("#{jenkins_extra_home}/.profile") do
  it { should contain %r|^eval \$(ssh-agent -s)| }
  it { should contain %r|^ssh-add \$HOME/\.ssh/\*.pem| }
end
