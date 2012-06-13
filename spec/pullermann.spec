$:.unshift File.join(File.dirname(__FILE__), '..', 'lib')
require 'pullermann'

describe Pullermann do

  before :each do
    # Variables to use inside the tests.
    @project = 'user/project'
    # Stub external dependency @gitconfig (local file).
    Pullermann.stub(:git_config).and_return(
      'github.login' => 'default_login',
      'github.password' => 'default_password',
      'remote.origin.url' => 'git@github.com:user/project.git'
    )
    # Stub external dependency @github (remote server).
    @github = mock 'GitHub'
    Octokit::Client.stub(:new).and_return(@github)
    @github.stub(:login)
    @github.stub(:api_version).and_return('3')
    @github.stub(:repo).with(@project)
  end

  after :each do
    # Empty all variables on Pullermann after each test.
    # Since we're not working with instances, this hack is necessary.
    Pullermann.instance_variables.each do |variable|
      Pullermann.instance_variable_set variable, nil
    end
  end

  it 'loops through all open pull requests' do
    @github.should_receive(:pulls).with(@project, 'open').and_return([])
    Pullermann.run
  end

  it 'checks existing comments to determine the last test run' do
    pull_request = mock 'pull request'
    request_id = 42
    pull_request.should_receive(:title).and_return('mock request')
    pull_request.should_receive(:mergeable).and_return(true)
    @github.stub(:pulls).and_return([{'number' => request_id}])
    @github.should_receive(:pull_request).with(@project, request_id).and_return(pull_request)
    # See if we're actually querying for issue comments.
    @github.should_receive(:issue_comments).with(@project, request_id).and_return([])
    # Skip the rest, as we will test this in other tests.
    Pullermann.stub(:switch_branch_to_merged_state)
    Pullermann.stub(:switch_branch_back)
    Pullermann.stub(:comment_on_github)
    Pullermann.run
  end

  it 'runs the tests when either source or target branch have changed'

  it 'posts comments to GitHub'

  it 'uses two different users for commenting (success/failure)'

  it 'updates existing comments to reduce noise'

  it 'deletes obsolete comments whenever the result changes'

  it 'allows for configuration by the user'

  it 'uses sane fall back values'

end
