#! /bin/sh

rm -f check_unattended_upgrades_patched
cp check_unattended_upgrades check_unattended_upgrades_patched
chmod a+x check_unattended_upgrades_patched
sed -i 's/ test / test_patched /g' check_unattended_upgrades_patched
