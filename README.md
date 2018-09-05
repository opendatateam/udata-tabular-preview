# Tabular Preview

A plugin to preview tabular files (CSV, Excel, ...) using [csvapi](https://github.com/opendatateam/csvapi)

## Usage

Install the plugin package in you udata environement:

```bash
pip install udata-tabular-preview
```

Then activate it in your `udata.cfg`:

```python
PLUGINS = ['tabular']
```

## Configuration

You can control this plugin behavior with the following `udata.cfg` parameters:

- **`TABULAR_CSVAPI_URL`**: The URL to your `csvapi` instance (without trailing slash). **ex:** `https://my.csvapi'
- **`TABULAR_UI`**:  Choose the UI displaying previews. You can choose between `csvapi-front` and `dataexplorer'. Default value is `csvapi-front`


## Development

### JS dependencies

Install JS dependencies with:

```shell
npm install
```

Then you can package these assets with:

```shell
inv assets
```

(You might need to relaunch these commands when you pull upstream changes).

### Python dependencies

Assuming you are in an active virtualenv with `udata` installed and in the current project cloned repository directory, install all dependencies using:

```shell
pip install -e requirements/develop.pip
```

(You might need to relaunch this command when you pull upstream changes).

### Testing

Tests are located into the `tests` folder and be run with:

```shell
inv test
```

### Quality

Code must pass Flake 8 validation and README should be compatible with `PyPI`.
You can check both with:

```shell
inv qa
```
