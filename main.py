import shutil, time, zipfile, os, datetime

vault = {
  'vaults': [
    {
      'name': 'TempVault',
      'root': './TempVault',
      'main_io': 'Main IO',
      'working_dir': 'Working',
      'backup_dir': 'Backups',
      'snapshot_dir': 'Snapshots',
      'restore_point_dir': 'Restore Points'
    }
  ],
  'current': 0
}

# Source and destination directories
src_dir = vault['vaults'][vault['current']]['root']+'/'+vault['vaults'][vault['current']]['main_io']
dst_dir = vault['vaults'][vault['current']]['root']+'/'+vault['vaults'][vault['current']]['working_dir']+'/Files'

# Interval in seconds between each copy
# interval = 60 * 60  # 1 hour
interval = 10

while True:
  now = datetime.datetime.now()
  try:
    # Copy all files and directories from source to destination
    shutil.rmtree(dst_dir)
    shutil.copytree(src_dir, dst_dir)
    print(f'Copied contents of {src_dir} to {dst_dir}')
    with zipfile.ZipFile(vault['vaults'][vault['current']]['root']+'/'+vault['vaults'][vault['current']]['working_dir']+'/temp.backup', 'w') as f:
      for root, dirs, files in os.walk(dst_dir):
        for dir in dirs:
          f.write(os.path.join(root, dir), os.path.join(root, dir).split(vault['vaults'][vault['current']]['root']+'/'+vault['vaults'][vault['current']]['working_dir']+'/Files')[1])
        for file in files:
          f.write(os.path.join(root, file), os.path.join(root, file).split(vault['vaults'][vault['current']]['root']+'/'+vault['vaults'][vault['current']]['working_dir']+'/Files')[1])
        f.close()
    
    shutil.copy(vault['vaults'][vault['current']]['root']+'/'+vault['vaults'][vault['current']]['working_dir']+'/temp.backup', vault['vaults'][vault['current']]['root']+'/'+vault['vaults'][vault['current']]['backup_dir']+now.strftime("/%Y\%m\%d %H:%M:%S.backup"))
    os.remove(vault['vaults'][vault['current']]['root']+'/'+vault['vaults'][vault['current']]['working_dir']+'/temp.backup')

    print('Created backup of the current vault')
  except Exception as e:
    print(f'Error while copying: {e}')

  # Wait for the interval before copying again
  time.sleep(interval)
