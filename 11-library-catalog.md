# 11. Каталог библиотеки и деклараций

Источники: `L/org/zenframework/z8/lang/*.bl`, `L/org/zenframework/z8/lang/sql/*.bl` и остальные `L/**/*.bl`; ревизия и обозначения — в [разделе 1](01-overview.md). Каталог автоматически получен из исходников на момент исследования. Это перечень объявленных строк и путей, не семантический разбор и не перечень доказанно работающих вызовов; видимость, наследование, перегрузка и поведение определяются проверками компилятора и реализацией. Многострочные объявления, если встретятся, могли не попасть в строковую выборку. Код библиотек может распространяться на условиях лицензии исходного проекта Z8.

## 11.1 Объявления базовых и SQL-типов

Для каждого файла приведены строки с открытыми или защищёнными объявлениями, оканчивающимися `;`; также оставлены заголовки классов, enum и привязки `[native]`/`[primary]`. Тела, комментарии и импорты исключены; унаследованные члены здесь не развёрнуты.

### `Attribute.bl`

Источник: `L/org/zenframework/z8/lang/Attribute.bl`.

```bl
[native "org.zenframework.z8.server.runtime.Attribute"]
public class Attribute {
static public string Name = "name";
static public string DisplayName = "displayName";
static public string Description = "description";
static public string Label = "label";
static public string Icon = "icon";
static public string Index = "index";
```

### `binary.bl`

Источник: `L/org/zenframework/z8/lang/binary.bl`.

```bl
[primary "org.zenframework.z8.server.types.binary"]
public final class binary extends primary {
public string name;
public string getName();
public binary setName(string name);
public string getBaseName();
public string getExtension();
public int length();
public static binary zip(file fileOrDirectory);
public static binary zip(binary[] binaries);
public void unzip(file directory);
public void unzip(file directory, encoding charset);
```

### `bool.bl`

Источник: `L/org/zenframework/z8/lang/bool.bl`.

```bl
[primary "org.zenframework.z8.server.types.bool"]
public final class bool extends primary {
public operator string();
public operator sql_bool();
public bool operator == (bool value);
public bool operator != (bool value);
public bool operator ! ();
public bool operator && (bool value);
public bool operator || (bool value);
static public bool parse(string string);
```

### `date.bl`

Источник: `L/org/zenframework/z8/lang/date.bl`.

```bl
[primary "org.zenframework.z8.server.types.date"]
public final class date extends primary {
static public date Min = '01/01/0001 00:00:00';
static public date Max = '01/01/5000 00:00:00';
static public date now();
static public date today();
static public date tomorrow();
static public date yesterday();
public operator string();
public operator sql_date();
public void operator = (int ticks);
public date operator + (datespan value);
public date operator - (datespan value);
public datespan operator - (date value);
public bool operator < (date value);
public bool operator > (date value);
public bool operator <= (date value);
public bool operator >= (date value);
public bool operator == (date value);
public bool operator != (date value);
static public bool isEqualDate(date date1, date date2);
public int ticks();
public int year();
public int quarter();
public int month();
public int weekOfYear();
public int day();
public int dayOfWeek();
public int dayOfYear();
public int daysInMonth();
public int hours();
public int minutes();
public int seconds();
public int milliseconds();
public int zoneOffset();
public void setDate(int year, int month, int day);
public void setTime(int hour, int minute, int second);
public void setTime(int hour, int minute, int second, int millisecond);
public void setZoneOffset(int zoneOffset);
public void set(int year, int month, int day, int hour, int minute, int second);
public void set(int year, int month, int day, int hour, int minute, int second, int millisecond);
public date addYear(int years);
public date addQuarter(int quarters);
public date addMonth(int months);
public date addDay(int days);
public date addHour(int hours);
public date addMinute(int minutes);
public date addSecond(int seconds);
public date addMillisecond(int milliseconds);
public date truncYear();
public date truncQuarter();
public date truncMonth();
public date truncDay();
public date truncHour();
public date truncMinute();
public date truncSecond();
public string toString(string frm);
public string toIsoString();
static public date parse(string timestamp);
static public date parseIsoString(string isoString);
static public date parse(string string, string frm);
```

### `datespan.bl`

Источник: `L/org/zenframework/z8/lang/datespan.bl`.

```bl
[primary "org.zenframework.z8.server.types.datespan"]
public final class datespan extends primary {
public operator string();
public operator sql_datespan();
public datespan operator + (datespan value);
public date operator + (date value);
public datespan operator - (datespan value);
public bool operator < (datespan value);
public bool operator > (datespan value);
public bool operator <= (datespan value);
public bool operator >= (datespan value);
public bool operator == (datespan value);
public bool operator != (datespan value);
public int days();
public int hours();
public int minutes();
public int seconds();
public int milliseconds();
public int totalHours();
public int totalMinutes();
public int totalSeconds();
public void setTotalHours(int hours);
public void setTotalMinutes(int minutes);
public void setTotalSeconds(int seconds);
public void set(int days, int hours, int minutes, int seconds);
public void set(int days, int hours, int minutes, int seconds, int milliseconds);
public void set(int ticks);
public void truncDay();
public void truncHour();
public void truncMinute();
public string toString(string frm);
static public datespan parse(string string);
```

### `decimal.bl`

Источник: `L/org/zenframework/z8/lang/decimal.bl`.

```bl
[primary "org.zenframework.z8.server.types.decimal"]
public final class decimal extends primary {
static public int RoundUp = 0;
static public int RoundDown = 1;
static public int RoundCeiling = 2;
static public int RoundFloor = 3;
static public int RoundHalfUp = 4;
static public int RoundHalfDown = 5;
static public int RoundHalfEven = 6;
static public int RoundUnnecessary = 7;
static public decimal Min;
static public decimal Max;
public operator string();
public operator sql_decimal();
public decimal operator + ();
public decimal operator - ();
public decimal operator + (int value);
public decimal operator - (int value);
public decimal operator * (int value);
public decimal operator / (int value);
public decimal operator % (int value);
public decimal operator + (decimal value);
public decimal operator - (decimal value);
public decimal operator * (decimal value);
public decimal operator / (decimal value);
public decimal operator % (decimal value);
public bool operator < (int value);
public bool operator > (int value);
public bool operator <= (int value);
public bool operator >= (int value);
public bool operator == (int value);
public bool operator != (int value);
public bool operator > (decimal value);
public bool operator < (decimal value);
public bool operator <= (decimal value);
public bool operator >= (decimal value);
public bool operator == (decimal value);
public bool operator != (decimal value);
public decimal abs();
public int signum();
public int ceil();
public int floor();
public int round();
public decimal round(int digits);
public decimal round(int digits, int mode);
public decimal sin();
public decimal cos();
public decimal tan();
public decimal asin();
public decimal acos();
public decimal atan();
public decimal sinh();
public decimal cosh();
public decimal tanh();
public decimal toRadians();
public decimal toDegrees();
public decimal exp();
public decimal ln();
public decimal log10();
public decimal sqrt();
public decimal cbrt();
public decimal power(decimal power);
static public decimal parse(string string);
```

### `encoding.bl`

Источник: `L/org/zenframework/z8/lang/encoding.bl`.

```bl
[native "org.zenframework.z8.server.types.encoding"]
public enum encoding {
```

### `exception.bl`

Источник: `L/org/zenframework/z8/lang/exception.bl`.

```bl
[primary "org.zenframework.z8.server.types.exception"]
public class exception {
public operator string();
virtual public string getMessage();
public string getStackTrace();
```

### `file.bl`

Источник: `L/org/zenframework/z8/lang/file.bl`.

```bl
[primary "org.zenframework.z8.server.types.file"]
public class file extends primary {
public guid id;
public string name;
public date time;
public int size;
public string path;
public guid user;
public string author;
public string[string] details;
public operator binary();
public operator string();
public void operator = (string path);
public bool operator == (file path);
public bool operator != (file path);
public bool exists();
public bool isEmpty();
public bool isFolder();
public file[] listFiles();
public file parent();
public string folder();
public string baseName();
public string fileName();
public string extension();
public date lastModified();
public string read();
public string read(encoding charset);
public file write(binary content);
public file write(string content);
public file write(string content, encoding charset);
public file append(binary content);
public file append(string content);
public file append(string content, encoding charset);
public void delete();
public void delete(bool recursively);
public file zip(file fileOrDirectory);
public file unzip(file directory);
public file unzip(file directory, encoding charset);
static public string name(string path);
static public string baseName(string path);
static public string extension(string path);
static public file[] parse(string json);
static public string toJson(file[] files);
static public file createTempFile(string prefix, string ext);
```

### `geometry.bl`

Источник: `L/org/zenframework/z8/lang/geometry.bl`.

```bl
[primary "org.zenframework.z8.server.types.geometry"]
public final class geometry extends primary {
static public final int DefaultSRS = 3857;
static public final int None = -1;
static public final int Ring = 0;
static public final int Point = 1;
static public final int Line = 2;
static public final int Polygon = 3;
static public final int MultiPoint = 4;
static public final int MultiLine = 5;
static public final int MultiPolygon = 6;
static public final int Collection = 7;
static public final string StrNone = "NONE";
static public final string StrRing = "RING";
static public final string StrPoint = "POINT";
static public final string StrLine = "LINE";
static public final string StrPolygon = "POLYGON";
static public final string StrMultiPoint = "MULTIPOINT";
static public final string StrMultiLine = "MULTILINE";
static public final string StrMultiPolygon = "MULTIPOLYGON";
static public final string StrCollection = "GEOMETRYCOLLECTION";
public int shape();
public int srs();
public geometry[] points();
public decimal x();
public decimal y();
public decimal[][] extent();
public geometry center();
public decimal length();
public decimal x1();
public decimal y1();
public decimal x2();
public decimal y2();
public decimal width();
public decimal height();
public string toGeoJson();
public operator string();
public operator sql_geometry();
public bool operator == (guid value);
public bool operator != (guid value);
static public geometry none(int srs);
static public geometry point(decimal x, decimal y, int srs);
static public geometry line(geometry[] points);
static public geometry multiLine(geometry[] lines);
static public geometry ring(geometry[] points);
static public geometry polygon(geometry[] rings);
static public geometry collection(geometry[] geometries);
static public geometry pointOnLine(geometry line, decimal distance);
static public geometry perpendicularToLine(geometry line, decimal distance, decimal length);
static public geometry fromHexString(string hexString);
static public geometry fromGeoJson(string geoJson, int srs);
static public geometry fromArray(geometry[] geometries);
```

### `guid.bl`

Источник: `L/org/zenframework/z8/lang/guid.bl`.

```bl
[primary "org.zenframework.z8.server.types.guid"]
public final class guid extends primary {
static public guid Null = '00000000-0000-0000-0000-000000000000';
static public guid create();
static public guid create(string value);
static public guid create(int minor);
static public guid create(int major, int minor);
public operator string();
public operator sql_guid();
public bool operator == (guid value);
public bool operator != (guid value);
public int minor();
public int major();
public int[] components();
static public guid parse(string value);
```

### `int.bl`

Источник: `L/org/zenframework/z8/lang/int.bl`.

```bl
[primary "org.zenframework.z8.server.types.integer"]
public final class int extends primary {
static public int Min = -0x7fffffffffffffff;
static public int Max =  0x7fffffffffffffff;
public operator decimal();
public operator string();
public operator sql_int();
public operator date();
public int operator ~ ();
public int operator + ();
public int operator - ();
public int operator + (int value);
public int operator - (int value);
public int operator * (int value);
public int operator / (int value);
public int operator % (int value);
public decimal operator + (decimal value);
public decimal operator - (decimal value);
public decimal operator * (decimal value);
public decimal operator / (decimal value);
public decimal operator % (decimal value);
public bool operator < (int value);
public bool operator > (int value);
public bool operator <= (int value);
public bool operator >= (int value);
public bool operator == (int value);
public bool operator != (int value);
public bool operator < (decimal value);
public bool operator > (decimal value);
public bool operator <= (decimal value);
public bool operator >= (decimal value);
public bool operator == (decimal value);
public bool operator != (decimal value);
public int operator & (int value);
public int operator | (int value);
public int operator ^ (int value);
public int abs();
public int signum();
public int and(int x);
public int or(int x);
public int xor(int x);
public int not();
public decimal sin();
public decimal cos();
public decimal tan();
public decimal asin();
public decimal acos();
public decimal atan();
public decimal sinh();
public decimal cosh();
public decimal tanh();
public decimal toRadians();
public decimal toDegrees();
public decimal exp();
public decimal ln();
public decimal log10();
public decimal sqrt();
public decimal cbrt();
public decimal power(decimal power);
public int leftShift(int _bit);
public int rightShift(int _bit);
public string toString(int radix);
public string toHexString();
public string toBinaryString();
static public int parse(string string);
static public int parse(string string, int radix);
```

### `Math.bl`

Источник: `L/org/zenframework/z8/lang/Math.bl`.

```bl
[native "org.zenframework.z8.server.math.Math"]
public final class Math {
static public final decimal PI;
static public int max(int a, int b);
static public decimal max(int a, decimal b);
static public decimal max(decimal a, int b);
static public decimal max(decimal a, decimal b);
static public int min(int a, int b);
static public decimal min(int a, decimal b);
static public decimal min(decimal a, int b);
static public decimal min(decimal a, decimal b);
static public date max(date a, date b);
static public date min(date a, date b);
static public decimal hypot(decimal x, decimal y);
static public decimal sin(decimal a);
static public decimal cos(decimal a);
static public decimal random();
```

### `Object.bl`

Источник: `L/org/zenframework/z8/lang/Object.bl`.

```bl
[native "org.zenframework.z8.server.runtime.OBJECT"]
public class Object {
static public User user();
static public User system();
virtual protected void constructor();
public guid key();
public string index();
public string name();
public string className();
public string id();
public void setId(string id);
public string displayName();
public void setDisplayName(string displayName);
public string getAttribute(string attribute);
public void setAttribute(string attribute, primary value);
public bool operator == (Object object);
public bool operator != (Object object);
virtual public string toString();
virtual public int compare(Object o);
virtual public void write(JsonWriter writer);
virtual protected binary processContentRequest(string[string] parameters, file[] files);
virtual protected JsonArray getData(string[string] parameters);
auto public Object[] objects;
public Object[] getNamed();
static public Object newInstance(string className);
static public Object newNamedInstance(string name);
static public Object getNamedSingleton(string name);
```

### `primary.bl`

Источник: `L/org/zenframework/z8/lang/primary.bl`.

```bl
[primary "org.zenframework.z8.server.types.primary"]
public class primary {
public string toString();
public int hashCode();
```

### `string.bl`

Источник: `L/org/zenframework/z8/lang/string.bl`.

```bl
[primary "org.zenframework.z8.server.types.string"]
public final class string extends primary {
public operator sql_string();
public operator exception();
public operator binary();
public operator file();
public string operator + (string value);
public bool operator < (string value);
public bool operator > (string value);
public bool operator <= (string value);
public bool operator >= (string value);
public bool operator == (string value);
public bool operator != (string value);
public int length();
public bool isEmpty();
public int compare(string anotherString);
public int compareNoCase(string anotherString);
public int indexOf(string subString);
public int indexOf(string subString, int offset);
public int lastIndexOf(string subString);
public int lastIndexOf(string subString, int offset);
public bool startsWith(string prefix);
public bool startsWith(string prefix, int offset);
public bool endsWith(string suffix);
public string charAt(int index);
public string substring(int index);
public string substring(int index, int count);
public string left(int count);
public string right(int count);
public string trim();
public string trimLeft();
public string trimRight();
public string padLeft(int length);
public string padLeft(int length, string padding);
public string padRight(int length);
public string padRight(int length, string padding);
public string insert(int pos, string what);
public string replace(int pos, int len, string replacement);
public bool matches(string regex);
public void setupMatcher(string regex);
public bool next();
public string getGroup(int groupNumber);
public string replaceFirst(string regex, string replacement);
public string replaceAll(string regex, string replacement);
public string[] split(string regex);
public string[] split(string regex, int limit);
public string toLowerCase();
public string toUpperCase();
public string firstToLowerCase();
public string firstToUpperCase();
static public string replicate(string str, int count);
static public string concat(string[] array, string delimeter);
static public string fromBinary(binary data);
static public string fromBinary(binary data, encoding encoding);
```

### `void.bl`

Источник: `L/org/zenframework/z8/lang/void.bl`.

```bl
[primary "void"]
public final class void {
```

### `sql/sql_binary.bl`

Источник: `L/org/zenframework/z8/lang/sql/sql_binary.bl`.

```bl
[primary "org.zenframework.z8.server.types.sql.sql_binary"]
public final class sql_binary extends sql_primary {
```

### `sql/sql_bool.bl`

Источник: `L/org/zenframework/z8/lang/sql/sql_bool.bl`.

```bl
[primary "org.zenframework.z8.server.types.sql.sql_bool"]
public final class sql_bool extends sql_primary {
public operator ();
public sql_bool operator == (sql_bool value);
public sql_bool operator != (sql_bool value);
public sql_bool operator ! ();
public sql_bool operator && (sql_bool value);
public sql_bool operator || (sql_bool value);
public sql_bool IIF(sql_bool yes, sql_bool no);
public sql_date IIF(sql_date yes, sql_date no);
public sql_datespan IIF(sql_datespan yes, sql_datespan no);
public sql_decimal IIF(sql_decimal yes, sql_decimal no);
public sql_guid IIF(sql_guid yes, sql_guid no);
public sql_int IIF(sql_int yes, sql_int no);
public sql_string IIF(sql_string yes, sql_string no);
public sql_geometry IIF(sql_geometry yes, sql_geometry no);
```

### `sql/sql_date.bl`

Источник: `L/org/zenframework/z8/lang/sql/sql_date.bl`.

```bl
[primary "org.zenframework.z8.server.types.sql.sql_date"]
public final class sql_date extends sql_primary {
public operator ();
public sql_int toInt();
public sql_date operator + (sql_datespan value);
public sql_date operator - (sql_datespan value);
public sql_datespan operator - (sql_date value);
public sql_bool operator < (sql_date value);
public sql_bool operator > (sql_date value);
public sql_bool operator <= (sql_date value);
public sql_bool operator >= (sql_date value);
public sql_bool operator == (sql_date value);
public sql_bool operator != (sql_date value);
public sql_int minute();
public sql_int hour();
public sql_int day();
public sql_int month();
public sql_int year();
public sql_date truncDay();
public sql_date truncHour();
public sql_date truncMinute();
public sql_date truncSecond();
public sql_date addDay(sql_int days);
public sql_date addHour(sql_int hours);
public sql_date addMinute(sql_int minutes);
public sql_date addSecond(sql_int seconds);
```

### `sql/sql_datespan.bl`

Источник: `L/org/zenframework/z8/lang/sql/sql_datespan.bl`.

```bl
[primary "org.zenframework.z8.server.types.sql.sql_datespan"]
public final class sql_datespan extends sql_primary {
public operator ();
public sql_date operator + (sql_date value);
public sql_datespan operator + (sql_datespan value);
public sql_datespan operator - (sql_datespan value);
public sql_bool operator < (sql_datespan value);
public sql_bool operator > (sql_datespan value);
public sql_bool operator <= (sql_datespan value);
public sql_bool operator >= (sql_datespan value);
public sql_bool operator == (sql_datespan value);
public sql_bool operator != (sql_datespan value);
public sql_int days();
public sql_int hours();
public sql_int minutes();
public sql_int seconds();
public sql_int totalHours();
public sql_int totalMinutes();
public sql_int totalSeconds();
public sql_datespan truncHour();
public sql_datespan truncMinute();
public sql_datespan truncSecond();
public sql_datespan addDay(sql_int days);
public sql_datespan addHour(sql_int hours);
public sql_datespan addMinute(sql_int minutes);
public sql_datespan addSecond(sql_int seconds);
```

### `sql/sql_decimal.bl`

Источник: `L/org/zenframework/z8/lang/sql/sql_decimal.bl`.

```bl
[primary "org.zenframework.z8.server.types.sql.sql_decimal"]
public final class sql_decimal extends sql_primary {
public operator ();
public sql_decimal operator + ();
public sql_decimal operator - ();
public sql_decimal operator + (sql_int value);
public sql_decimal operator - (sql_int value);
public sql_decimal operator * (sql_int value);
public sql_decimal operator / (sql_int value);
public sql_decimal operator % (sql_int value);
public sql_decimal operator + (sql_decimal value);
public sql_decimal operator - (sql_decimal value);
public sql_decimal operator * (sql_decimal value);
public sql_decimal operator / (sql_decimal value);
public sql_decimal operator % (sql_decimal value);
public sql_bool operator < (sql_int value);
public sql_bool operator > (sql_int value);
public sql_bool operator <= (sql_int value);
public sql_bool operator >= (sql_int value);
public sql_bool operator == (sql_int value);
public sql_bool operator != (sql_int value);
public sql_bool operator < (sql_decimal value);
public sql_bool operator > (sql_decimal value);
public sql_bool operator <= (sql_decimal value);
public sql_bool operator >= (sql_decimal value);
public sql_bool operator == (sql_decimal value);
public sql_bool operator != (sql_decimal value);
public sql_bool isNaN();
public sql_int sign();
public sql_decimal abs();
public sql_int ceil();
public sql_int floor();
public sql_decimal exp();
public sql_decimal ln();
public sql_decimal power(sql_int power);
public sql_decimal round(sql_int digits);
public sql_decimal truncate(sql_int digits);
```

### `sql/sql_geometry.bl`

Источник: `L/org/zenframework/z8/lang/sql/sql_geometry.bl`.

```bl
[primary "org.zenframework.z8.server.types.sql.sql_geometry"]
public final class sql_geometry extends sql_primary {
public operator ();
public sql_bool operator == (sql_geometry value);
public sql_bool operator != (sql_geometry value);
public sql_bool operator && (sql_geometry value);
public sql_int collectionSize();
public sql_decimal x();
public sql_decimal xMax();
public sql_decimal xMin();
public sql_decimal y();
public sql_decimal yMax();
public sql_decimal yMin();
public sql_decimal length();
public sql_geometry element(sql_int n);
public sql_geometry split(sql_geometry splitter);
public sql_geometry extract(sql_int type);
public sql_string strType();
public sql_bool intersects(sql_geometry geom);
public sql_geometry intersect(sql_geometry geom);
public sql_decimal distance(sql_geometry geom);
public sql_geometry startPoint();
public sql_geometry endPoint();
public sql_geometry union();
public sql_geometry centroid();
public sql_geometry homogenize();
public sql_geometry interpolatePoint(sql_decimal fraction);
public sql_geometry buffer(sql_decimal radius);
public sql_bool isEmpty();
public sql_bool isValid();
public sql_geometry makeValid();
public sql_string asGeoJSON();
public static sql_geometry point(sql_decimal x, sql_decimal y, sql_int srs);
```

### `sql/sql_guid.bl`

Источник: `L/org/zenframework/z8/lang/sql/sql_guid.bl`.

```bl
[primary "org.zenframework.z8.server.types.sql.sql_guid"]
public final class sql_guid extends sql_primary {
public operator ();
public sql_bool operator == (sql_guid value);
public sql_bool operator != (sql_guid value);
```

### `sql/sql_int.bl`

Источник: `L/org/zenframework/z8/lang/sql/sql_int.bl`.

```bl
[primary "org.zenframework.z8.server.types.sql.sql_integer"]
public final class sql_int extends sql_primary {
public operator ();
public operator sql_decimal();
public sql_int operator - ();
public sql_int operator + ();
public sql_int operator + (sql_int value);
public sql_int operator - (sql_int value);
public sql_int operator * (sql_int value);
public sql_int operator / (sql_int value);
public sql_int operator % (sql_int value);
public sql_decimal operator + (sql_decimal value);
public sql_decimal operator - (sql_decimal value);
public sql_decimal operator * (sql_decimal value);
public sql_decimal operator / (sql_decimal value);
public sql_decimal operator % (sql_decimal value);
public sql_bool operator < (sql_int value);
public sql_bool operator > (sql_int value);
public sql_bool operator <= (sql_int value);
public sql_bool operator >= (sql_int value);
public sql_bool operator == (sql_int value);
public sql_bool operator != (sql_int value);
public sql_bool operator < (sql_decimal value);
public sql_bool operator > (sql_decimal value);
public sql_bool operator <= (sql_decimal value);
public sql_bool operator >= (sql_decimal value);
public sql_bool operator == (sql_decimal value);
public sql_bool operator != (sql_decimal value);
public sql_int operator ~ ();
public sql_int operator & (sql_int value);
public sql_int operator | (sql_int value);
public sql_int operator ^ (sql_int value);
public sql_int sign();
public sql_int abs();
public sql_int power(sql_int power);
```

### `sql/sql_primary.bl`

Источник: `L/org/zenframework/z8/lang/sql/sql_primary.bl`.

```bl
[primary "org.zenframework.z8.server.types.sql.sql_primary"]
public class sql_primary {
public sql_string toString();
```

### `sql/sql_string.bl`

Источник: `L/org/zenframework/z8/lang/sql/sql_string.bl`.

```bl
[primary "org.zenframework.z8.server.types.sql.sql_string"]
public final class sql_string extends sql_primary {
public operator ();
public sql_string operator + (sql_string value);
public sql_bool operator < (sql_string value);
public sql_bool operator > (sql_string value);
public sql_bool operator <= (sql_string value);
public sql_bool operator >= (sql_string value);
public sql_bool operator == (sql_string value);
public sql_bool operator != (sql_string value);
public sql_bool isInt();
public sql_bool isNumeric();
public sql_int toInt();
public sql_decimal toDecimal();
public sql_date toDate();
public sql_bool isEmpty();
public sql_int length();
public sql_int indexOf(sql_string pattern);
public sql_int indexOf(sql_string pattern, sql_int position);
public sql_bool contains(sql_string pattern);
public sql_bool contains(sql_string pattern, sql_int position);
public sql_int patIndexOf(sql_string reg_exp);
public sql_bool like(sql_string pattern);
public sql_bool like(sql_string pattern, sql_string escape);
public sql_bool regLike(sql_string pattern);
public sql_string toLower();
public sql_string toUpper();
public sql_string trimLeft();
public sql_string trimRight();
public sql_string trimAll();
public sql_string padLeft(sql_int length);
public sql_string padLeft(sql_int length, sql_string pattern);
public sql_string padRight(sql_int length);
public sql_string padRight(sql_int length, sql_string pattern);
public sql_string replace(sql_string pattern, sql_string replacement);
public sql_string replaceAll(sql_string pattern, sql_string replacement);
public sql_string replaceAll(sql_string pattern, sql_string replacement, sql_string flags);
public sql_string substring(sql_int position, sql_int count);
public sql_string reverse();
public sql_string quote();
public sql_string json(sql_string name);
public sql_string json(sql_int num);
public sql_bool ftsLike(sql_string query);
public sql_bool ftsLike(sql_string query, Fts fts);
public sql_decimal ftsRank(sql_string query);
public sql_decimal ftsRank(sql_string query, Fts fts);
```

## 11.2 Файлы библиотеки фреймворка

Каждая строка — путь относительно `L/`; имя файла определяет имя единицы компиляции, а не обязательно полное API. Индекс не доказывает применимость файла в любой конфигурации зависимостей.

- `org/zenframework/z8/base/application/Application.bl`
- `org/zenframework/z8/base/application/Resources.bl`
- `org/zenframework/z8/base/application/ServerConfig.bl`
- `org/zenframework/z8/base/crypto/Base34.bl`
- `org/zenframework/z8/base/crypto/Digest.bl`
- `org/zenframework/z8/base/crypto/MD5.bl`
- `org/zenframework/z8/base/entity/Entity.bl`
- `org/zenframework/z8/base/entity/EntityParser.bl`
- `org/zenframework/z8/base/entity/EntityTable.bl`
- `org/zenframework/z8/base/entity/Filter.bl`
- `org/zenframework/z8/base/entity/Registry.bl`
- `org/zenframework/z8/base/entity/Visitor.bl`
- `org/zenframework/z8/base/eval/Eval.bl`
- `org/zenframework/z8/base/Executable.bl`
- `org/zenframework/z8/base/file/AttachmentProcessor.bl`
- `org/zenframework/z8/base/file/FileConverter.bl`
- `org/zenframework/z8/base/file/FileHandler.bl`
- `org/zenframework/z8/base/form/action/Action.bl`
- `org/zenframework/z8/base/form/action/ActionReport.bl`
- `org/zenframework/z8/base/form/action/ActionType.bl`
- `org/zenframework/z8/base/form/action/Parameter.bl`
- `org/zenframework/z8/base/form/action/ParameterSource.bl`
- `org/zenframework/z8/base/form/ActionGroup.bl`
- `org/zenframework/z8/base/form/Control.bl`
- `org/zenframework/z8/base/form/Desktop.bl`
- `org/zenframework/z8/base/form/FieldGroup.bl`
- `org/zenframework/z8/base/form/Fieldset.bl`
- `org/zenframework/z8/base/form/Form.bl`
- `org/zenframework/z8/base/form/LabelAlign.bl`
- `org/zenframework/z8/base/form/Listbox.bl`
- `org/zenframework/z8/base/form/report/CustomData.bl`
- `org/zenframework/z8/base/form/report/DataSource.bl`
- `org/zenframework/z8/base/form/report/Range.bl`
- `org/zenframework/z8/base/form/report/Report.bl`
- `org/zenframework/z8/base/form/Section.bl`
- `org/zenframework/z8/base/form/Selector.bl`
- `org/zenframework/z8/base/form/Source.bl`
- `org/zenframework/z8/base/form/Tab.bl`
- `org/zenframework/z8/base/form/TabControl.bl`
- `org/zenframework/z8/base/fts/Fts.bl`
- `org/zenframework/z8/base/fts/FtsQueryType.bl`
- `org/zenframework/z8/base/json/Json.bl`
- `org/zenframework/z8/base/json/JsonArray.bl`
- `org/zenframework/z8/base/json/JsonObject.bl`
- `org/zenframework/z8/base/json/JsonPath.bl`
- `org/zenframework/z8/base/json/JsonUtil.bl`
- `org/zenframework/z8/base/json/JsonWriter.bl`
- `org/zenframework/z8/base/ldap/LdapAPI.bl`
- `org/zenframework/z8/base/ldap/LdapGroup.bl`
- `org/zenframework/z8/base/ldap/LdapUser.bl`
- `org/zenframework/z8/base/poi/Cell.bl`
- `org/zenframework/z8/base/poi/Row.bl`
- `org/zenframework/z8/base/poi/Sheet.bl`
- `org/zenframework/z8/base/poi/Workbook.bl`
- `org/zenframework/z8/base/query/Period.bl`
- `org/zenframework/z8/base/query/Query.bl`
- `org/zenframework/z8/base/query/ReadLock.bl`
- `org/zenframework/z8/base/security/LoginParameters.bl`
- `org/zenframework/z8/base/security/Role.bl`
- `org/zenframework/z8/base/security/SecurityEvent.bl`
- `org/zenframework/z8/base/security/SecurityLog.bl`
- `org/zenframework/z8/base/security/SecurityObject.bl`
- `org/zenframework/z8/base/security/User.bl`
- `org/zenframework/z8/base/sql/Connection.bl`
- `org/zenframework/z8/base/sql/Cursor.bl`
- `org/zenframework/z8/base/sql/Database.bl`
- `org/zenframework/z8/base/sql/Transaction.bl`
- `org/zenframework/z8/base/table/RecordLock.bl`
- `org/zenframework/z8/base/table/SchemaGenerator.bl`
- `org/zenframework/z8/base/table/Sequencer.bl`
- `org/zenframework/z8/base/table/SortDirection.bl`
- `org/zenframework/z8/base/table/Sql.bl`
- `org/zenframework/z8/base/table/system/Domains.bl`
- `org/zenframework/z8/base/table/system/Entries.bl`
- `org/zenframework/z8/base/table/system/Fields.bl`
- `org/zenframework/z8/base/table/system/Files.bl`
- `org/zenframework/z8/base/table/system/Requests.bl`
- `org/zenframework/z8/base/table/system/RoleFieldAccess.bl`
- `org/zenframework/z8/base/table/system/RoleRequestAccess.bl`
- `org/zenframework/z8/base/table/system/Roles.bl`
- `org/zenframework/z8/base/table/system/RoleTableAccess.bl`
- `org/zenframework/z8/base/table/system/Sequences.bl`
- `org/zenframework/z8/base/table/system/Settings.bl`
- `org/zenframework/z8/base/table/system/Tables.bl`
- `org/zenframework/z8/base/table/system/UserEntries.bl`
- `org/zenframework/z8/base/table/system/UserRoles.bl`
- `org/zenframework/z8/base/table/system/Users.bl`
- `org/zenframework/z8/base/table/system/view/RoleTableAccessView.bl`
- `org/zenframework/z8/base/table/system/view/UserForm.bl`
- `org/zenframework/z8/base/table/system/view/UsersView.bl`
- `org/zenframework/z8/base/table/Table.bl`
- `org/zenframework/z8/base/table/TreeTable.bl`
- `org/zenframework/z8/base/table/value/Aggregation.bl`
- `org/zenframework/z8/base/table/value/AttachmentField.bl`
- `org/zenframework/z8/base/table/value/BinaryField.bl`
- `org/zenframework/z8/base/table/value/BoolExpression.bl`
- `org/zenframework/z8/base/table/value/BoolField.bl`
- `org/zenframework/z8/base/table/value/CountExpression.bl`
- `org/zenframework/z8/base/table/value/DateExpression.bl`
- `org/zenframework/z8/base/table/value/DateField.bl`
- `org/zenframework/z8/base/table/value/DatespanExpression.bl`
- `org/zenframework/z8/base/table/value/DatespanField.bl`
- `org/zenframework/z8/base/table/value/DatetimeExpression.bl`
- `org/zenframework/z8/base/table/value/DatetimeField.bl`
- `org/zenframework/z8/base/table/value/DecimalExpression.bl`
- `org/zenframework/z8/base/table/value/DecimalField.bl`
- `org/zenframework/z8/base/table/value/ExchangeRateField.bl`
- `org/zenframework/z8/base/table/value/Expression.bl`
- `org/zenframework/z8/base/table/value/Field.bl`
- `org/zenframework/z8/base/table/value/FieldType.bl`
- `org/zenframework/z8/base/table/value/FileExpression.bl`
- `org/zenframework/z8/base/table/value/FileField.bl`
- `org/zenframework/z8/base/table/value/GeometryExpression.bl`
- `org/zenframework/z8/base/table/value/GeometryField.bl`
- `org/zenframework/z8/base/table/value/GuidExpression.bl`
- `org/zenframework/z8/base/table/value/GuidField.bl`
- `org/zenframework/z8/base/table/value/IntExpression.bl`
- `org/zenframework/z8/base/table/value/IntField.bl`
- `org/zenframework/z8/base/table/value/Join.bl`
- `org/zenframework/z8/base/table/value/JoinType.bl`
- `org/zenframework/z8/base/table/value/JsonObjectExpression.bl`
- `org/zenframework/z8/base/table/value/Link.bl`
- `org/zenframework/z8/base/table/value/LinkExpression.bl`
- `org/zenframework/z8/base/table/value/MoneyField.bl`
- `org/zenframework/z8/base/table/value/NowField.bl`
- `org/zenframework/z8/base/table/value/StringExpression.bl`
- `org/zenframework/z8/base/table/value/StringField.bl`
- `org/zenframework/z8/base/table/value/TextExpression.bl`
- `org/zenframework/z8/base/table/value/TextField.bl`
- `org/zenframework/z8/base/table/value/TimestampField.bl`
- `org/zenframework/z8/base/table/value/TodayField.bl`
- `org/zenframework/z8/ie/DataMessage.bl`
- `org/zenframework/z8/ie/FileMessage.bl`
- `org/zenframework/z8/ie/ImportPolicy.bl`
- `org/zenframework/z8/ie/Message.bl`
- `org/zenframework/z8/justintime/table/CompileAction.bl`
- `org/zenframework/z8/justintime/table/JustInTimeTools.bl`
- `org/zenframework/z8/justintime/table/Source.bl`
- `org/zenframework/z8/justintime/table/SourcesView.bl`
- `org/zenframework/z8/lang/Attribute.bl`
- `org/zenframework/z8/lang/binary.bl`
- `org/zenframework/z8/lang/bool.bl`
- `org/zenframework/z8/lang/date.bl`
- `org/zenframework/z8/lang/datespan.bl`
- `org/zenframework/z8/lang/decimal.bl`
- `org/zenframework/z8/lang/encoding.bl`
- `org/zenframework/z8/lang/exception.bl`
- `org/zenframework/z8/lang/file.bl`
- `org/zenframework/z8/lang/geometry.bl`
- `org/zenframework/z8/lang/guid.bl`
- `org/zenframework/z8/lang/int.bl`
- `org/zenframework/z8/lang/Math.bl`
- `org/zenframework/z8/lang/Object.bl`
- `org/zenframework/z8/lang/primary.bl`
- `org/zenframework/z8/lang/sql/sql_binary.bl`
- `org/zenframework/z8/lang/sql/sql_bool.bl`
- `org/zenframework/z8/lang/sql/sql_date.bl`
- `org/zenframework/z8/lang/sql/sql_datespan.bl`
- `org/zenframework/z8/lang/sql/sql_decimal.bl`
- `org/zenframework/z8/lang/sql/sql_geometry.bl`
- `org/zenframework/z8/lang/sql/sql_guid.bl`
- `org/zenframework/z8/lang/sql/sql_int.bl`
- `org/zenframework/z8/lang/sql/sql_primary.bl`
- `org/zenframework/z8/lang/sql/sql_string.bl`
- `org/zenframework/z8/lang/string.bl`
- `org/zenframework/z8/lang/void.bl`
- `org/zenframework/z8/utils/Cron.bl`
- `org/zenframework/z8/utils/Sorter.bl`

Методы коллекций, добавляемые компилятором, не представлены в этих `.bl`; их сигнатуры приведены в [разделе 9](09-library.md).
