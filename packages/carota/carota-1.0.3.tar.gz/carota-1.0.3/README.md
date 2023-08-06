# carota: random data CSV generator

`carota` is a simple random data CSV generator. The project is [hosted on PyPi](https://pypi.org/project/carota/).

## Installation

```bash
pip install carota
```

## Usage

`carota` can be used from the command line

```bash
$ carota
1,12c27ffa-e3d2-4047-9bd9-9f51ad4f5bef,Leon,Conner,33,2020-11-24 07:41:58
2,e602242f-6523-4a4b-a98d-be0d369560a2,Sammie,Meyers,19,2020-11-24 02:05:07
3,b02315f5-d958-453f-8caa-bf240941549c,Edwina,Huynh,23,2020-11-24 02:24:38
4,7cd2b600-90c6-4fd3-83ad-ccccaacb28a2,Jane,Odom,20,2020-11-24 15:44:17
5,db68160c-9071-4e96-a694-aaae4abdd59e,Sammie,Spears,86,2020-11-24 21:01:08
6,27ad021e-a4c0-40eb-be01-12c77c0786d7,Hershel,Ferguson,31,2020-11-24 07:25:13
7,8c8c90d0-be3e-4955-a7fe-d7124576ec7f,Emogene,Mcdonald,77,2020-11-24 14:19:52
8,88cc3b5d-b492-4920-9254-402215ce623e,Ola,Lam,78,2020-11-24 21:23:27
9,65c04452-8fc4-4613-8d18-cd7288dfde08,Dexter,Frazier,82,2020-11-24 18:04:38
10,d1aa329f-5c25-4b71-abce-926d72ad28f5,Grover,Caldwell,62,2020-11-24 10:58:27
```

or it can be imported in a Python file

```python
>>> from carota import carota
>>> c = carota.carota()
>>> type(c)
<class 'generator'>
>>> next(c)
'1,08013c7a-48ab-4dea-89e9-6cfbcaa1198e,Linda,Brooks,86,2020-11-24 05:46:22.9924216'
>>> next(c)
'2,d101366d-c4dd-40b9-92cb-0428e130cdb7,Loyal,Tanner,40,2020-11-24 22:56:38.6393126'
>>> next(c)
'3,e33d7468-0a3c-4071-94ac-472f64a1fd1f,Agnes,Zavala,23,2020-11-24 07:33:38.1772276'
```

## Arguments

`carota` takes below arguments:

```text
  -r, --rows        Number of rows, defaults to 10
  -t, --text        Text to generate from built-in fields,
                    defaults to <index; uuid; firstname; lastname; int::start=18,end=95; date::delta=365>
  -d, --delimiter   Delimiter, defaults to ','
  -e, --encloser    Encloser, default the empty string
  -o, --output      output filepath, defaults to STDOUT
  -c, --chunck-size count of rows to write to file at a time, defaults to 100000
  --append          Append to file instead of overwrite
```

### Built-in fields

`carota` has a good few built-in fields that can take options. These built-ins are concatenated and passed to the `text` argument.

Multiple fields are separated with `;`.
Options are passed with `::`, assigned with `=` and separated with `,`.

Example `field1; field2::option1=value1,option2=value2; field3`

| field     | description                                    | options | default value           |
|-----------|------------------------------------------------|---------|-------------------------|
| index     | row number                                     | start   | 1                       |
| constant  | repeats same value                             | value   |                         |
| choice    | pick from list of possible value               | list    |                         |
|           |                                                | weight  |                         |
| int       | generate int                                   | start   | 0                       |
|           |                                                | end     | 100                     |
|           |                                                | seed    | None                    |
| string    | generate string                                | size    | 40                      |
| date      | generate date                                  | start   | today's date            |
|           |                                                | delta   | 365                     |
|           |                                                | format  | %Y-%m-%d %H:%M:%S.%f6   |
| uuid      | generate UUID                                  | seed    | None                    |
| tel       | generate tel number with format (###) ###-#### |         |                         |
| ssn       | generate SSN with format ###-##-####           |         |                         |
| lastname  | generate lastname                              |         |                         |
| firstname | generate firstname                             | gender  | 'f' or 'm'              |
| gender    | generate gender ('F' or 'M')                   |         |                         |

### Example

```bash
# generate a file with 1 million rows with index, UUID and a 6 digit number.
$ carota -r 1000000 -t "index; choices::list=true false,weights=2 1; uuid; int::start=100000,end=999999" -d ';' -e '"' -o uuid.csv
$ head uuid.csv
"1";"true";"bbbc2a2d-3c4a-4523-942a-2317a2de4cb4";"693839"
"2";"true";"7b159c9c-2645-4e1d-957c-371aa2aacf31";"831373"
"3";"true";"9deaecce-1f62-4d1d-90db-14da371f0368";"162622"
"4";"false";"40cb4ab9-8002-4a6c-a456-9f23abd8efe6";"132698"
"5";"true";"8f142044-eccd-44ac-b472-f97f8cb4f60d";"845696"
"6";"true";"f9d89ad7-b5ea-4b1f-b8da-238b90328d82";"150960"
"7";"false";"101910b9-05d4-4ab9-b788-ab571d17d8ad";"361464"
"8";"true";"0b4a1c4b-448b-4d63-8184-30ecc7950f63";"606203"
"9";"true";"0a543239-1bf0-4e1d-9587-38572471dd3e";"650516"
"10";"true";"a3d732ae-4f21-4194-a424-e0148e66e96b";"516921"
```

## License

This project is released under [GNU GENERAL PUBLIC LICENSE V3](https://www.gnu.org/licenses/gpl-3.0.en.html).
