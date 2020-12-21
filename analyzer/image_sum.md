# Как я это сделал
- Нейронка взята отсюда: [Imagecaptioning](https://github.com/ruotianluo/ImageCaptioning.pytorch#generate-image-captions)
Немного видоизменил чтобы запускалось без gpu.
- Используем претренированную сеть
  [FC](https://github.com/ruotianluo/ImageCaptioning.pytorch/blob/master/MODEL_ZOO.md)
- Есть еще несколько моментов которые нужно скачать и свести в нужных
  метсах, детали опущу, все есть в архиве

## Зависимости
- pip3 install yacs
- pip3 install lmdbdict
- pip3 install gensim
- pip3 install tensorflow
- pip3 install keras


Может что-то еще, зависит от того что у тебя уже установлено. Будет
ругаться на то что чего-то нет - устанавливай или пиши мне


## нужны, но уже в архиве. трогать не нужно скорее всего
- [cider](https://github.com/ruotianluo/cider/tree/e9b736d038d39395fa2259e39342bb876f1cc877)
- [coco captions](https://github.com/ruotianluo/coco-caption/tree/ea20010419a955fed9882f9dcc53f2dc1ac65092)

# Как использовать.

1. Помещаем изображение в папку blah
2. Запускаем нейронку командой -
 python3 tools/eval.py --model model.pth --infos\_path infos.pkl --image\_folder blah --num\_images-1 --device cpu --language\_eval 0
3. Результаты помещаются в vis/vis.json
4. ВАЖНО! Из-за какого-то бага нужно после каждого запуска нейронки
   нужно удалять файл eval\_results/.saved\_pred\_fc\_test.pth
5. Удаляем изображение из blah
