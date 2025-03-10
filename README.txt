Site Cloner Kullanım Kılavuzu (Turkish)

Genel Bilgi:Bu Python betiği, belirli bir web sitesini klonlamak için kullanılır. Site Cloner, bir sayfanın tamamını veya belirli varlıkları (HTML, CSS, JS, img) indirerek yerel olarak saklamanızı sağlar.

Kurulum:

Python'un kurulu olduğundan emin olun. (Python 3.6+ önerilir)

Gerekli bağımlılıkları yükleyin:

pip install -r requirements.txt

Scripti terminal veya komut satırında çalıştırın.

Kullanım:

1. Tek Bir Sayfa Klonlamak

python site_cloner.py "https://ornek-site.com"

Bu komut, yalnızca ana sayfayı ve onun varlıklarını (CSS, JS, görseller) indirir.

2. Tüm Siteyi Klonlamak (--full parametresi)

python site_cloner.py "https://ornek-site.com" --full

Bu komut, tüm siteyi (örneğin, ornek.com/register, ornek.com/about) ve iç bağlantıları ile birlikte indirir.

3. Çerez Kullanarak Sayfa Klonlamak

Eğer site çerez gerektiriyorsa, şu şekilde çerezleri iletebilirsiniz:

python site_cloner.py "https://ornek-site.com" --cookies "sessionid=xyz123; userid=456"

4. Çıktıyı Belirli Bir Klasöre Kaydetmek

python site_cloner.py "https://ornek-site.com" --output "my_cloned_site"

Bu komut, tüm dosyaları my_cloned_site/ klasörüne kaydeder.

Özellikler:

✅ HTML, CSS, JS, img gibi varlıkları indirir.

✅ Alt dizinleri koruyarak organize eder.

✅ Tüm iç linkleri tarayarak bağlantılı sayfaları indirir (--full).

✅ Çerez desteğiyle özel oturumları taklit eder.

✅ İndirme ilerlemesini ve yüzde tamamlanma durumunu gösterir.

