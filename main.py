import shutil, time, zipfile, os, datetime

# Interval in seconds between each copy
# interval = 60 * 60  # 1 hour
interval = 10

class vault:
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
      
      shutil.copy(vault.data['vaults'][vault_number]['root']+'/'+vault.data['vaults'][vault_number]['dirs']['working']['root']+'/temp.'+vault.data['vaults'][vault_number]['file_ext']['backup'], vault.data['vaults'][vault_number]['root']+'/'+vault.data['vaults'][vault_number]['dirs']['backup']+now.strftime("/%Y %m %d %H %M %S.")+vault.data['vaults'][vault_number]['file_ext']['backup'])
      os.remove(vault.data['vaults'][vault_number]['root']+'/'+vault.data['vaults'][vault_number]['dirs']['working']['root']+'/temp.'+vault.data['vaults'][vault_number]['file_ext']['backup'])
      temp = vault.data['vaults'][vault_number]['name']
      print(f'Created backup of the files in the vault \'{temp}\'')
      del temp
    except Exception as e:
      print(f'Error while copying: {e}')

while True:
  for i in vault.data['active_vaults']:
    vault.backup(i)

  # Wait for the interval before copying again
  time.sleep(interval)
