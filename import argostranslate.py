import argostranslate.package
import argostranslate.translate

argostranslate.package.update_package_index()

available_packages = argostranslate.package.get_available_packages()

package_to_install = next(
    (pkg for pkg in available_packages if pkg.from_code == "en" and pkg.to_code == "pl"),
    None
)

if package_to_install:
    download_path = package_to_install.download()
    argostranslate.package.install_from_path(download_path)
    print("Model EN → PL został pomyślnie zainstalowany.")
else:
    print("Nie znaleziono modelu EN → PL.")