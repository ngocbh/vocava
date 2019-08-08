# vocava

Mọi người trước khi push thì tạo branch mới mang tên phần mình làm rồi push lên

### App
push app lên thư mục app, nhớ ignore các file build ko cần thiết.

### Service
Gồm 3 phần:
* speech to text
* ocr
* task generator

Công việc còn lại của phần task generator: 
* Thiết kế database ở file ```server/database/mongo_models.py```
* User.topics là danh sách các topic mà người dùng hay đọc, mình nên làm kiểu người dùng có thể tự add topic vào và mình tự phân tích từ các tài liệu người dùng hay đọc.
* thêm topic cho từng từ, các từ có khả năng nằm trong topic nào, cái này tìm cách sửa từ init_database, nghĩa là làm sẵn trước cho toàn bộ các từ trước đi, rồi đoạn
```
word = Dictionary(index=str(row['lemma']), level=cur_level, sfi=sfi, wordlist=str(row['wordlist']))
``` 
trong ```init_database.py``` thì thêm tham số ```topics=get_topics(str['lemma'])``` vào. cần viết thêm hàm get_topics, hiện tại chưa có. Viết hàm này thì để vào thư mục service vì coi vụ xử lý topic như service task_generator 

* Trong bộ phân tích hiện tại, mới chỉ lấy ra các từ unknown_word theo kiểu lấy ( priority + num_search (xem WordWrapper ```mongo_models```) ) từ cao xuống thấp. hiện tại 2 giá trị này đều bằng 0. Sau này khi làm xong cái vụ tính toán số lần ấn vào màn hình của mỗi từ thì cập nhật trường num_search còn priority là dựa vào topic, có thể dùng theo kiểu priority là số topic của từ trùng với số topic của người dùng hoặc là độ tương tự của topic người dùng so vs topic của từ, có thể dùng hàm path_similarity() của wordnet.

* Chưa có cập nhật kết quả exam. nghĩa là khi tạo 1 exam trong hàm ```generate_exam()``` thì tạo 1 exam id cho nó, rồi lưu vào Exam document đã viết sẵn trong mongo_models.
* Khi người dùng làm xong bài kiểm tra thì trả lại user ( android ) gửi 1 lệnh POST kết quả lên cho server ( viết 1 api kiểu get_result để nhận kết quả và tăng độ ma_score ( khả năng hiểu của người dùng đối với 1 từ ) ) chuyển các từ đã đại ma_score tối đa sang known_word, thêm các từ mới mà mình phân tích được bù vào mục unknow_word ( các từ tiếp theo có cùng level hoặc các từ có topics theo mình là nên học, sửa các chỉ số như priority và num_search để từ đó có thể xuất hiện trong exam tiếp theo )


### Requirements

Install mongodb, for unix user:
```
brew install mongodb
```

Start mongodb service
```
brew service start mongodb
```

Install python package:
```
pip3 install -r requirements.txt
```
or
```
python3 -m pip install -r requirements.txt
```

### Instruction to run
Init database
```
python3 -m server.databases.init_databases
```
Run server:
```
./run-dev
```

### API Guide
```IP_ADDRESS``` is your IP_ADDRESS in your lan. example : ```192.168.1.23``` check by ```ifconfig```, to connect from other device you need to  turn off firewall of server machine and connect to same network ( wifi or lan )
Test server on local machine, you can use ```localhost``` or ```0.0.0.0``` instead.
#### Home 
```
http://IP_address:3000/
```

#### Get dictionary

Get all words in dictionary
```
/api/dictionary
```
full api example:
```
http://IP_ADDRESS:3000/api/dictionary
```

#### Get UserInfo
Get user info by user-id, for example user-id = 1
```
/api/user-info?id=1
```

#### Get Oxford Result with specific word
```
/api/get-oxford-result?word=hello
```
#### Get Exam for specific user
```
/api/create-new-exam?user-id=1
```
đưa tham số là user-id, hệ thống sẽ phân tích và tạo ra bài kiểm tra là danh sách các task như ở dưới

#### Get specific task for specific word
6 task: definition, definition-task, pronunciation-task, sentence-task, puzzle-task, practice-task

##### Definition
```
/api/create-definition?word=quiz
```

example result (JSON):
```
{
  "antonyms": [], 
  "shortDefinition": "test of knowledge", 
  "synonyms": [
    "test", 
    "quiz"
  ], 
  "type": "definition", 
  "word": "quiz"
}
```
Kết quả trả về bao gồm dạng task, từ , định nghĩa ngắn, từ đồng nghĩa, từ trái nghĩa -> cho người dùng nhìn từ, và định nghĩa của nó, bên cạnh đó cho người dùng xem qua các từ đồng nghĩa có level thấp hơn ( để người dùng có thể hình dung nghĩa của từ )

##### Definition task
```
/api/create-definition-task?word=quiz
```

example result (JSON):
```
{
  "answer": 1, 
  "options": [
    "dock", 
    "quiz", 
    "grid", 
    "flaw"
  ], 
  "question": "test of knowledge", 
  "type": "definition_task", 
  "word": "quiz"
}
```
Kết quả trả về bao gồm dạng task, từ , định nghĩa của từ, 4 từ là các câu trả lời trắc nghiệm, và vị trí của đáp án



##### Pronunciation task
```
/api/create-pronunciation-task?word=quiz
```

example result (JSON):
```
{
  "answer": 2, 
  "explainAnswer": "kwɪz", 
  "options": [
    "explicitly", 
    "canal", 
    "quiz", 
    "flourish"
  ], 
  "question": "http://audio.oxforddictionaries.com/en/mp3/quiz_gb_1.mp3", 
  "type": "pronunciation_task", 
  "word": "quiz"
}
```
Kết quả trả về bao gồm dạng task, từ , link tới file audio của từ, 4 từ là các câu trả lời trắc nghiệm, và vị trí của đáp án, sau khi người dùng nhập đáp án thì hiện explainAnswer là phát cách đọc của từ theo bang IPA

##### Sentence task
```
/api/create-sentence-task?word=quiz
```

example result (JSON):
```
{
  "answer": 0, 
  "options": [
    "quiz", 
    "bishop", 
    "tighten", 
    "flaw"
  ], 
  "question": "a sports ___ ", 
  "type": "sentence_task", 
  "word": "quiz"
}
```
Kết quả trả về bao gồm dạng task, từ , 1 câu về từ cần hỏi, đã thay thế = '\_\_\_', 4 câu trả lời trắc nghiệm, và vị trí của đáp án,
cẩn thận với loại task này vì vẫn còn lỗi chưa khắc phục đc. 1 là do các dạng khác của từ trong câu, vd khi học về từ query nhưng trong câu chỉ có queies thì question ko biến đc từ queies thành ___ . tiếp theo là như cái câu mẫu, câu a sports ____ quá chung chung, ko thể hiện đc tính chất của từ quiz


##### Puzzle task
```
/api/create-puzzle-task?word=quiz
```

example result (JSON):
```
{
  "answer": "quiz", 
  "options": [
    "i", 
    "z", 
    "q", 
    "u"
  ], 
  "question": "http://audio.oxforddictionaries.com/en/mp3/quiz_gb_1.mp3", 
  "type": "puzzle_task", 
  "word": "quiz"
}
```
Kết quả trả về bao gồm dạng task, từ , link tới file audio của từ, options là các chữ cái đã bị xáo trộn, answer là từ, khi làm cần kiểm tra xem người dùng viết thứ tự của từ có đúng ko?


##### Practice task
```
/api/create-practice-task?word=quiz
```

random 1 trong 4 cái bài kiểm tra kia để kiểm tra lại



