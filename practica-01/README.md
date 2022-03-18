# Práctica 1

## [Kaggle API](https://github.com/Kaggle/kaggle-api)

To use the Kaggle API, sign up for a Kaggle account at https://www.kaggle.com. Then go to the 'Account' tab of your user profile (`https://www.kaggle.com/<username>/account`) and select 'Create API Token'. This will trigger the download of `kaggle.json`, a file containing your API credentials. Place this file in the location `~/.kaggle/kaggle.json` (on Windows in the location `C:\Users\<Windows-username>\.kaggle\kaggle.json` - you can check the exact location, sans drive, with `echo %HOMEPATH%`). You can define a shell environment variable `KAGGLE_CONFIG_DIR` to change this location to `$KAGGLE_CONFIG_DIR/kaggle.json` (on Windows it will be `%KAGGLE_CONFIG_DIR%\kaggle.json`).

## Acerca de

Script de python para descargar automáticamente los datos con los que se trabajarán de kaggle.

## Instalación

Para ejecutar el proyecto hay que instalar las librerías listadas en el archivo de texto con el siguiente comando:

```
pip install -r requirements.txt
```

> `python -m venv env`
