# Talk doser

Extract data from talking between two people, following the Whatsapp formatting.
Support talking between 2 peoples only for now.

## Use

Import conversation file at the project root.

Create `secrets.json` file, following this schema:

```json
{
  "file": "./file-name.txt",
  "people": [
    {
      "pseudo": "person 1",
      "display": "Person 1"
    },
    {
      "pseudo": "person 2",
      "display": "Person 2"
    }
  ]
}
```

Then run the main script:

```bash
$ python3.6 doser.py
```
