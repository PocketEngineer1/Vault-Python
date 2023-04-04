import shutil, time, zipfile, os, datetime, PySimpleGUI as sg, sys, threading

# Interval in seconds between each copy
# interval = 60 * 60  # 1 hour
interval = 10

class vault:
  handler_kill_switch = False
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
    'vault_ids': [0],
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
        print(f'Error: {e}')
  
  def handler():
    while True:
      if vault.handler_kill_switch:
        break

      i = len(vault.data['vaults'])
      while i > 0:
        i = i - 1
        vault.backup(i)

      # Wait for the interval before copying again
      time.sleep(interval)
      pass

  def gui():
    global window
    sg.theme('DefaultNoMoreNagging')   # Add a touch of color
    # All the stuff inside your window.
    layout = [
      [sg.Text('Select a directory:')],
      [sg.Input(key='-FOLDER-'), sg.FolderBrowse()],
      [sg.Button('List Directory')],
      [sg.Listbox(values=[], size=(40, 10), key='-FILE LIST-')],
      [sg.Button('Exit')]
    ]

    # Create the Window
    window = sg.Window(f'Vault [Python {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}] [PySimpleGUI {sg.__version__}]', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
      event, values = window.read()
      if event == sg.WIN_CLOSED or event == 'Cancel' or event == 'Exit': # if user closes window or clicks cancel
        vault.handler_kill_switch = True
        break
      if event == 'List Directory':
        folder_path = values['-FOLDER-']
        if os.path.isdir(folder_path):
          file_list = os.listdir(folder_path)
          window['-FILE LIST-'].update(file_list)
        else:
          sg.popup(f"The path '{folder_path}' is not a directory.", title="That's not a directory!")

if __name__ == '__main__':
  while_thread = threading.Thread(target=vault.handler)
  tkinter_thread = threading.Thread(target=vault.gui)
    
  while_thread.start()
  tkinter_thread.start()
    
  while_thread.join()
  tkinter_thread.join()
