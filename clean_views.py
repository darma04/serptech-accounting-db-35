"""Remove all orphaned service/sparepart code from views.py."""
import re

with open('apps/laporan/views.py', encoding='utf-8') as f:
    content = f.read()

# Find the last 'return context' of LaporanStokDetailView
# Then remove everything after it until the SECOND '# LAPORAN CABANG' header
# The pattern is:
# 1. Last return context before the orphaned code
# 2. All the orphaned service body + sparepart class
# 3. First occurrence of '# LAPORAN CABANG' header (the one we inserted)  
# 4. Keep only the second '# LAPORAN CABANG' header

# Strategy: Find all positions of '# LAPORAN CABANG' header
cabang_matches = list(re.finditer(r'# ═+[\s\S]*?#  LAPORAN CABANG', content))
print(f"Found {len(cabang_matches)} CABANG headers")

# Remove from the last 'return context' (of StokDetailView) through the first CABANG header,
# keeping only the second CABANG header (the real one)
stok_return_idx = content.rfind('        return context\n\n', 0, content.find('class LaporanCabangView'))
if stok_return_idx >= 0:
    # Find where the orphaned code ends - at the second CABANG header
    if len(cabang_matches) >= 2:
        first_cabang_start = cabang_matches[0].start()
        second_cabang_start = cabang_matches[1].start()
        
        # Remove everything from stok_return_idx to second_cabang_start
        before = content[:stok_return_idx]
        after = content[second_cabang_start:]
        new_content = before + after
        
        with open('apps/laporan/views.py', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Removed {second_cabang_start - stok_return_idx} chars of orphaned code")
    else:
        print("Could not find second CABANG header")
else:
    print("Could not find StokDetailView return context")

# Verify
with open('apps/laporan/views.py', encoding='utf-8') as f:
    final = f.read()
cabang_count = final.count('LAPORAN CABANG')
service_count = final.count('LaporanServiceView')
sparepart_count = final.count('LaporanSparepartView')
print(f"After cleanup: CABANG headers={cabang_count}, ServiceView={service_count}, SparepartView={sparepart_count}")
