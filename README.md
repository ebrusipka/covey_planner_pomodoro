 Covey Matrix ve Pomodoro Zamanlayıcı

Bu, Covey Matrisi kullanarak görev yönetimini ve Pomodoro Zamanlayıcısını birleştiren bir Python uygulamasıdır. Kullanıcıların görevleri önem ve aciliyet durumlarına göre organize etmelerine ve odaklanmış çalışma seansları için Pomodoro zamanlayıcılarını kullanmalarına olanak tanır.

Özellikler

- Covey Matrisi: Görevleri önem ve aciliyet durumlarına göre dört bölüme ayırın.
- *Görev Yönetimi: Görev ekleme, silme ve güncelleme. Görevler için notlar, tarih ve tekrar seçenekleri ekleyin.
- Pomodoro Zamanlayıcı: Pomodoro seansları, kısa molalar ve uzun molalar için zamanlayıcılar içerir.
- Görev Filtreleme: Bugünkü görevler, bu haftaki görevler, bu ayki görevler, tamamlanmamış görevler ve daha fazlası gibi çeşitli kriterlere göre görevleri filtreleyin.
- Görev İlerlemesi: Her görevin ilerlemesini izleyin ve %25'lik artışlarla güncelleyin.
- Bildirimler: Pomodoro seansları tamamlandığında bildirim alın.
- Veri Sürekliliği Görevleri JSON dosyasına kaydedin ve yükleyin.

Gereksinimler

- Python 3.x
- `tkinter` kütüphanesi
- `tkcalendar` kütüphanesi
- `plyer` kütüphanesi
- `threading` ve `time` modülleri
- `datetime` modülü
- `json` modülü
- `os` modülü
 Kurulum

1. Depoyu klonlayın:
    ```sh
 https://github.com/ebrusipka/covey_planner_pomodoro/blob/main/covey_planner_pomodoro.py
    ```

2. Gerekli kütüphaneleri yükleyin:
    ```sh
    pip install tkcalendar plyer
    ```

Kullanım

 Uygulamayı çalıştırın:
    ```sh
    python covey_matrix_pomodoro.py
    ```

   Görev Ekleme:
    - Görev detaylarını (tarih, görev adı, önem, aciliyet, not ve tekrar) doldurun.
    - Görevi ilgili bölüme eklemek için "Görev Ekle" butonuna tıklayın.

   Görev Yönetimi:
    - Görevleri filtrelemek için açılır menüyü kullanarak bugünkü görevler, bu haftaki görevler, bu ayki görevler, tamamlanmamış görevler ve daha fazlasını görüntüleyin.
    - Görevleri tamamlandı olarak işaretlemek için görev yanındaki kutucuğu işaretleyin.
    - Görev ilerlemesini "+25%" butonuyla güncelleyin.
    - Görev ilerlemesini "Sıfırla" butonuyla sıfırlayın.
    - Notları görüntülemek için "Notu Göster" butonuna tıklayın.
    - Görevleri silmek için "Sil" butonuna tıklayın.

   Pomodoro Zamanlayıcısını Kullanma:
    - "Pomodoro", "Kısa Mola" veya "Uzun Mola" sekmelerinden birini seçin.
    - Zamanlayıcıyı başlatmak için "Başlat" butonuna tıklayın.
    - Zamanlayıcıyı sıfırlamak için "Sıfırla" butonuna tıklayın.

   Görevleri Kaydetme ve Yükleme:
    - Görevler otomatik olarak mevcut dizindeki `tasks.json` dosyasına kaydedilir.
    - Uygulama başlatıldığında görevler `tasks.json` dosyasından yüklenir.

Dosya Yapısı

- `covey_matrix_pomodoro.py`: Covey Matrix ve Pomodoro Zamanlayıcı mantığını içeren ana uygulama dosyası.
- `tasks.json`: Görevlerin kalıcı olarak saklandığı JSON dosyası.




1. Depoyu kopyalayın.
2. Özellik veya hata düzeltmesi için yeni bir dal oluşturun.
3. Değişikliklerinizi yapın.


