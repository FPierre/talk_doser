# Talk doser

> Note: currently in Proof of Concept state.

* Extract data from talking between people.
* Following the Whatsapp text formatting: dd/mm/YYYY, h:m - person_pseudo blah blah blah

## Setup

Export Whatsapp talking.

Import Whatsapp talking file at the project root.

Create `secrets.json` file, following this schema:

```json
{
  "file": "./talking-file-name.txt",
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

Run the main script:

```bash
$ python3.6 doser.py
```
