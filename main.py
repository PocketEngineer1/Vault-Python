import shutil, time, zipfile, os, datetime, sys, threading, pygame
from UI_Framework import *

class vault:
  handler_active = False
  # Interval in seconds between each copy
  # interval = 60 * 60  # 1 hour
  interval = 10
  data = {
    'vaults': [
      {
        'name': 'TempVault',
        'root': './TempVault',
        'file_ext': {
          'backup': 'backup',
          'snapshot': 'snapshot',
          'restore_point': 'restore'
        },
        'dirs':{
          'main_io': 'Main IO',
          'backup': 'Backups',
          'snapshot': 'Snapshots',
          'restore_point': 'Restore Points',
          'working': {
            'root': 'Working',
            'files': 'Files'
          }
        }
      }
    ],
    'active_vaults': [0]
  }

  def backup(vault_number: int):
    if vault_number in vault.data['active_vaults']:
      # Source and destination directories
      src_dir = vault.data['vaults'][vault_number]['root']+'/'+vault.data['vaults'][vault_number]['dirs']['main_io']
      dst_dir = vault.data['vaults'][vault_number]['root']+'/'+vault.data['vaults'][vault_number]['dirs']['working']['root']+'/'+vault.data['vaults'][vault_number]['dirs']['working']['files']

      now = datetime.datetime.now()
      try:
        # Copy all files and directories from source to destination
        shutil.rmtree(dst_dir)
        shutil.copytree(src_dir, dst_dir)
        print(f'Copied contents of {src_dir} to {dst_dir}')
        with zipfile.ZipFile(vault.data['vaults'][vault_number]['root']+'/'+vault.data['vaults'][vault_number]['dirs']['working']['root']+'/temp.backup', 'w') as f:
          for root, dirs, files in os.walk(dst_dir):
            for dir in dirs:
              f.write(os.path.join(root, dir), os.path.join(root, dir).split(vault.data['vaults'][vault_number]['root']+'/'+vault.data['vaults'][vault_number]['dirs']['working']['root']+'/Files')[1])
            for file in files:
              f.write(os.path.join(root, file), os.path.join(root, file).split(vault.data['vaults'][vault_number]['root']+'/'+vault.data['vaults'][vault_number]['dirs']['working']['root']+'/Files')[1])
            f.close()
        
        shutil.copy(vault.data['vaults'][vault_number]['root']+'/'+vault.data['vaults'][vault_number]['dirs']['working']['root']+'/temp.'+vault.data['vaults'][vault_number]['file_ext']['backup'], vault.data['vaults'][vault_number]['root']+'/'+vault.data['vaults'][vault_number]['dirs']['backup']+now.strftime("/%Y-%m-%d %H-%M-%S.")+vault.data['vaults'][vault_number]['file_ext']['backup'])
        os.remove(vault.data['vaults'][vault_number]['root']+'/'+vault.data['vaults'][vault_number]['dirs']['working']['root']+'/temp.'+vault.data['vaults'][vault_number]['file_ext']['backup'])
        temp = vault.data['vaults'][vault_number]['name']
        print(f'Created backup of the files in the vault \'{temp}\'')
        del temp
      except Exception as e:
        temp = vault.data['vaults'][vault_number]['name']
        print(f'An error ocurred with the vault named \"{temp}\"\n{e}')
  
  def handler():
    print("Vault handler started!")
    while vault.handler_active:
      i = len(vault.data['vaults'])
      while i > 0:
        i = i - 1
        vault.backup(i)

      # Wait for the interval before starting again
      time.sleep(vault.interval)
      pass

  class GUI:
    title = f'Vault [Python {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}] [PyGame {pygame.__version__}]'

    def handler():
      print("Vault GUI starting...")
      def unnamed_function():
        print('')
      ui = UI((800, 600), vault.GUI.title)
      button = Button((100, 100), (200, 50), (255, 0, 0), 'Click me!', click_handler=unnamed_function)
      ui.add_button(button)
      print("Vault GUI started!")
      ui.run()
      

if __name__ == '__main__':
  vault_handler_thread = threading.Thread(target=vault.handler)
  vault_gui_thread = threading.Thread(target=vault.GUI.handler)
    
  # vault_handler_thread.start()
  vault_gui_thread.start()
    
  # vault_handler_thread.join()
  vault_gui_thread.join()
