import os
import glob
import json
from SublimeLinter.lint import Linter  # or NodeLinter, PythonLinter, ComposerLinter, RubyLinter


class SublimeLinterClangTidy(Linter):
    regex = (
        r'^.+?:(?P<line>\d+):(?P<col>\d+): '
        r'(?:(?P<error>error)|(?P<warning>warning)): '
        r'(?P<message>.+)'
    )
    multiline = False
    defaults = {
        'selector': 'source.c, source.c++'
    }
    build_json_list = []

    def make_json_list(self):
      for open_folder in self.view.window().folders():
        for build_folder in glob.glob(open_folder+"/build*"):
          json_file = build_folder + '/compile_commands.json'
          if( os.path.exists(json_file)):
            self.build_json_list.append(build_folder)

    def get_command_location(self, file_name):
      if( len(self.build_json_list) == 0 ):
        self.make_json_list();

      for compile_commands in self.build_json_list:
        with open(compile_commands+'/compile_commands.json','r') as f:
          data = json.load(f)
          for datum in data:
            if (datum['file'] == file_name):
              return compile_commands

    def cmd(self):
      json_location = self.get_command_location(self.view.file_name())
      if( json_location == None ):
        print('cannot file json file for '+ self.view.file_name())
        return []

      return ['clang-tidy', '-quiet', '-p={}'.format(json_location),
        self.view.file_name()]


