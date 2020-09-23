#!/usr/bin/env ruby

require 'prophet'
require 'logger'
require 'yaml'
require_relative 'ci_executor'

Prophet.setup do |config|
  # Setup Github access.
  CONFIG_FILE = './options.yml'

  if File.exists?(CONFIG_FILE)
    options = YAML.load_file(CONFIG_FILE)

    config.username_pass = options['default']['username_pass']
    config.access_token_pass = options['default']['access_token_pass']

    config.username_fail = options['default']['username_fail']
    config.access_token_fail = options['default']['access_token_fail']
  end

  # Setup logging.
  config.logger = log = @logger = Logger.new(STDOUT)
  log.level = Logger::INFO

  # Now that GitHub has fixed their notifications system, we can dare to increase
  # Prophet's verbosity and use a new comment for every run.
  config.reuse_comments = false

  config.comment_failure = 'Prophet reports failure.'
  config.comment_success = 'Well Done! Your tests are still passing.'

  # Specify which tests to run. (Defaults to `rake test`.)
  # NOTE: Either ensure the last call in that block runs your tests
  # or manually set @result to a boolean inside this block.
  config.execution do
    executor = SCC::CiExecutor.new(logger: config.logger)
    executor.run!

    config.success = executor.success?

    if config.success
      log.info 'All tests are passing.'
    else
      config.comment_failure += "\n#{executor.fail_message}"
      log.info 'Some tests are failing.'
      executor.inspect_failed

      throw RuntimeError, config.comment_failure
    end
  end
end

# Finally, run Prophet!
Prophet.run
