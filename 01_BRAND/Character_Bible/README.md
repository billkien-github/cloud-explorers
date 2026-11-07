# Character Bible

Nguồn chuẩn cho mọi thông tin về nhân vật. Concept: [`cloud_explorers_character_sheet.png`](cloud_explorers_character_sheet.png) và ảnh trong `02_ASSET_LIBRARY/Characters/<Tên>/concept/` (`_hero` có bối cảnh; ảnh nền trơn, ảnh xoay `_turnaround` làm tham chiếu Seedance và ảnh dựng model: `02_ASSET_LIBRARY/MODELING.md`).

**Nhóm Cloud Explorers:** khám phá những vùng đất kỳ diệu · giải mã bí ẩn của thế giới · học hỏi, sáng chế và trải nghiệm · tạo ra vô vàn tình huống dở khóc dở cười.

**Thế giới:** Fantasy + Science. Đảo đá bay giữa mây, thác nước, chùa tháp mái cong, cây hoa hồng (`01_BRAND/Brand_Guideline/world_key_art.png`). Cầu nối giữa phép thuật và máy móc là **tinh thể phát sáng**. Căn cứ Wonder Hub, Chronicle Engine và Story Portal: `03_CONTENT/README.md`. Tạo hình **soft stylized**: tròn, mềm, pastel, đầu to (gần bằng nửa chiều cao).

## Nhân vật

| | **LUMO** | **TAVI** | **NORI** | **PIKO** |
|---|---|---|---|---|
| Danh hiệu | Cáo Mây | Nhà Phát Minh | Tinh Linh Ánh Sáng | Bóng Nước Kỳ Quặc |
| Vai | Explorer, mở đầu phiêu lưu | Inventor, ra giải pháp | Story Keeper, kiến thức | Wild Card, **động cơ gây hài** |
| Tính cách | Tò mò, năng động, luôn khởi xướng phiêu lưu | Thiên tài sáng chế, thích lắp ráp, thử nghiệm, nhiều ý tưởng "điên rồ" | Điềm đạm, tinh tế, giàu kiến thức, đưa ra manh mối và góc nhìn mới | Tinh nghịch, háu ăn, đáng yêu, cực kỳ khó đoán |
| Chất hài | Hấp tấp, làm trước nghe sau | Giải pháp phức tạp cho việc đơn giản | Giải thích dài, bị ngắt lời | Chạm lung tung, dễ phân tâm vì đồ lấp lánh, hay gây bất ngờ "ngoài kịch bản" |
| Ngoại hình | Cáo, tai rất to (trong hồng, ngoài cam tới tận chóp), chỏm lông màu kem trên đầu, mắt nâu to, bụng và mõm màu kem, đuôi bông màu cam chóp kem | Bò sát nhỏ, bụng kem, **gai tinh thể** dọc lưng và đuôi, mắt xanh lá | Khối tròn phát sáng, đầu liền thân, **4 cánh trong suốt**, 2 râu đầu ngôi sao vàng, tay nhỏ, vệt sáng thay chân | Khối thạch trong suốt, 2 sừng xanh đậm, tay nhỏ, giọt nước bắn quanh người |
| Đồ đeo | Áo choàng đỏ dài tới gối, viền hoa văn mây vàng, khuy tròn vàng, đuôi thò ra qua khe xẻ giữa lưng áo; túi da đeo chéo có hình mây | Mũ phi công da + kính bảo hộ, áo gile kem nhiều túi, thắt lưng, đeo Inventor Pack giữa lưng, dưới hàng gai lớn ở đầu và vai | — | Pocket of Wonders: túi nhỏ cao khoảng 0.2 L (khoảng 1/4 chiều cao Piko, to hơn quả táo một chút), đeo chéo: dây vàng quàng qua gốc sừng phải, chạy dọc lưng, vòng chéo dưới miệng; túi ở hông trái, ngang tầm tay (ảnh `piko_pouch_ref.png` mặt trước, `piko_pouch_ref_back.png` mặt sau) |
| Dáng | Đứng, đi 2 chân | Đứng, đi 2 chân, chân ngắn, có đuôi | **Bay, không chân** | **Không chân**, nảy và trườn trên đất |
| Chiều cao | 1.00 (chuẩn) | 0.85 | 0.70 | 0.80 |
| Màu tham chiếu | Lông cam `#FD8A2B`, kem `#FEECCF`, áo choàng `#FC6640` | Da `#84B746`, bụng `#EFCB99`, tinh thể `#14F5F4` | Thân `#E8C3FB`, cánh `#D3ABFC`, sao `#FEF7A0` | Thân `#44DAFC` → `#06CFFD`, lưỡi `#D23C55` |

Chiều cao trên hình: `cast_lineup.png` (cạnh file này) xếp bốn nhân vật cùng đường chân, cao đúng tỉ lệ bảng trên, ghép từ ảnh đủ đồ bằng `pipeline/turnaround.py --cao` (ảnh đủ đồ đổi thì ghép lại). Băng nhóm trên `cloud_explorers_character_sheet.png` vẽ Nori, Piko nhỏ hơn tỉ lệ này, chỉ dùng để lấy phong cách.

Mã màu lấy mẫu ở vùng được chiếu sáng của ảnh tham chiếu trong `concept/` (cùng bộ với ảnh xoay Seedance đang dùng), dùng làm điểm xuất phát khi làm material.

**Chờ chốt:**
- Chiều cao đo tới đâu (đỉnh đầu hay chóp tai, chóp sừng, râu). Previz 2D hiện đo tới chóp: Tavi và Piko gần bằng nhau.
- Piko lúc khô (chưa có nước) có ẩn các giọt nước quanh người không. Previz 2D Cảnh 1 tập 01 đang ẩn tới khi Piko húp giọt sương.

**Nhân vật nền: sinh vật nhỏ của Thung lũng Mây** (có mặt từ Cảnh 1 tập 01). Thân tròn hình hạt đậu màu be hồng nhạt, bụng sáng hơn, mắt chấm, tay chân ngắn, không sừng, không cánh, không đuôi; mỗi con đội một chiếc lá khô làm mũ; cao khoảng 1/6 Lumo. Đứng nền, không tranh khung với bốn nhân vật chính. Concept 4 tư thế (ủ rũ, thở dài, chạy che lá to, té nước): `02_ASSET_LIBRARY/Characters/Valley_Critters/concept/valley_critters_ref.png`.

**Nhân vật nền: chú chim nhỏ** (EP000A). Lông nâu hạt dẻ, bụng kem, má hồng, chỏm lông trên đầu, chỏm đuôi cuộn tròn, cỡ bằng nắm tay Lumo. Không nói, chỉ kêu "CHÍP"; cười bằng cách lấy cánh vỗ bụng. Màu tránh tím, vàng sao của Nori và xanh thạch của Piko. Ảnh xoay: `02_ASSET_LIBRARY/Characters/Little_Bird/concept/little_bird_turnaround.png`.

**Nhân vật nền: bướm phát sáng** (EP000A). Bướm nhỏ cỡ một ngón tay Lumo, cánh hồng đào nhạt phát sáng mềm. Màu tránh tím, vàng sao của Nori, vàng của Wonder Compass và xanh ngọc tín hiệu của hòn đảo Wonder Hub, để không lẫn với Nori và với ánh sáng dẫn truyện. Concept ba tư thế (xoè cánh, bay, đậu): `02_ASSET_LIBRARY/Characters/Glow_Butterflies/concept/glow_butterflies_ref.png`.

**Nhân vật nền: quyển sách nhỏ** (EP000C). Một quyển sách sống cỡ bằng nửa thân Nori, bìa vải đỏ gạch sẫm, gáy và bốn góc bọc da nâu sẫm, giấy màu kem, hai mắt tròn trên bìa trước, không miệng, không tay chân, một dải ruy băng kem đánh dấu trang thò ra ở mép dưới các trang, cong lên như cái đuôi. Bay bằng cách vỗ hai bìa như cánh chim. Không nói; vui thì giũ trang sột soạt, giận hay ngại thì gập bìa lại (BỘP!). Tinh nghịch, mê truyện phiêu lưu, hay trốn khỏi giá để đọc.

**Nhân vật nền: sách bay** (EP000C). Sách trong thư viện cổ bay như đàn chim, vỗ bìa như cánh, không có mặt; nhiều cỡ, bìa màu trầm (nâu, kem, đỏ gạch nhạt, xám tro); quyển to nhất là quyển sách cổ bìa nâu dày, góc bọc đồng, cao bằng cả người Nori. Không tranh khung với Nori và quyển sách nhỏ. Đây là tính chất của sách trong thư viện, không phải phép của Nori: nghe ai gọi tên chủ đề thì một quyển thuộc chủ đề đó bay tới người gọi; gọi "tất cả" kèm chủ đề thì cả đàn sách thuộc chủ đề đó bay tới cùng lúc; gọi kèm số giá hay "lên giá" thì những quyển được gọi bay về đúng giá. Quyển quá to thì bay chậm, chao đảo, có thể rơi.

**Nhân vật phụ: bà Gấu bán bánh** (EP000D). Gấu tròn, hiền, lông nâu sữa, mõm kem, tạp dề kem có túi to phía trước; cao khoảng 1.3 Lumo. Bán bánh bao mật ong ở khu chợ nổi, hấp trong xửng đặt trên một viên đá tinh thể ấm phát sáng hổ phách (không lửa). Nói chậm, ít, hay cười. Màu tránh cam của Lumo và xanh lá của Tavi.

**Nhân vật nền: cá mây** (EP000D). Cá nhỏ bơi trong không trung trên biển mây như bơi trong nước. Thân tròn trắng ngà ánh xà cừ, vây và đuôi mỏng như voan, mắt to, má chấm hồng. Cá mẹ dài bằng nửa Piko; ba cá con cỡ quả mận, chưa bơi xa được, ở trong một cái giỏ đan cũ làm tổ. Không nói, chỉ kêu "PIP"; mê đồ ăn. Màu tránh xanh ngọc tín hiệu của hòn đảo, tím và vàng sao của Nori, xanh thạch của Piko.

**Cặp quan hệ tạo chuyện:** Lumo ↔ Tavi (vội vàng vs cẩn thận) · Tavi ↔ Nori (máy móc vs nguồn gốc) · Nori ↔ Piko (trật tự vs hỗn loạn) · **Lumo ↔ Piko** (cặp gây hài nhiều nhất).

## Bảo bối

| Bảo bối | Của | Công dụng | Giới hạn |
|---|---|---|---|
| Wonder Compass | Lumo | Cảm nhận được điều kỳ lạ | Không biết đó là gì |
| Inventor Pack | Tavi | Mỗi lần lắp được 1 máy (thiết bị, công cụ…) | Cần thời gian, hay xảy ra lỗi |
| Story Lens | Nori | Cho manh mối, gợi ý | Vẫn phải tự suy luận, giải mã |
| Pocket of Wonders | Piko | Lấy ra những vật phẩm bất ngờ | Không kiểm soát được thứ mình lấy ra |

Concept: `02_ASSET_LIBRARY/Props/<Tên>/concept/`.

**Mũi sao** của Wonder Compass là ngôi sao tám cánh xoay được trên mặt la bàn. Một cánh là đầu chỉ: dài gần gấp rưỡi các cánh khác, vàng kim sáng, đầu có viên đá xanh nhỏ. Bảy cánh còn lại ngắn bằng nhau, trắng xanh.

**Wonder Compass báo hiệu thế nào** (giữ nguyên mọi tập): mũi sao luôn quay về điều kỳ lạ, dù xoay la bàn hay người cầm đi vòng (la bàn thật thì chỉ hướng Bắc). Càng gần thì la bàn càng sáng, rung mạnh, kêu TÍT TÍT TÍT. Điều kỳ lạ ở xa lóe sáng thì la bàn lóe theo cùng nhịp. Điều kỳ lạ ở gần đã tắt thì mũi sao chuyển sang điều kỳ lạ kế tiếp; còn kỳ lạ thì mũi sao nằm yên chỉ về nó. La bàn không chỉ đường đi, không báo nguy hiểm.

**Story Lens cho manh mối thế nào** (giữ nguyên mọi tập): Nori cầm cán, đưa mặt kính lên trước mắt, nhìn một thứ. Bình thường nhìn qua kính chỉ thấy mọi thứ to hơn một chút, ánh tím nhạt, như qua kính lúp. Nhìn vào thứ đang giấu một bí ẩn mà Nori muốn hiểu, mặt kính sáng lên và hiện **một hình gợi ý**: hình vẽ đơn giản kiểu tranh sách truyện, một vật hay một ý (cái bập bênh, bông tuyết), không chữ, không mũi tên. Khán giả thấy hình qua cú cận mặt kính. Hình giữ vài giây rồi mờ đi; nhìn lại đúng thứ đó chỉ hiện lại hình cũ, không thêm gì. Hình chỉ gợi ý, không phải câu trả lời: Nori phải tự nối hình với những gì quanh mình. Kính không chỉ đường, không chiếu hình ra ngoài, không làm vật bên ngoài sáng lên, không đọc chữ, không báo nguy hiểm, không cho thấy tương lai. Hòn đảo Wonder Hub lóe xanh ngọc thì mặt kính lóe xanh ngọc cùng nhịp (Season 0, như Wonder Compass). Story Lens trông như kính lúp nên không bao giờ hướng về phía mặt trời, và nằm trong nắng cũng không hội tụ thành chấm sáng trên giấy hay vật nào (trẻ không bắt chước soi kính lúp ngoài nắng).

**Inventor Pack hoạt động thế nào** (giữ nguyên mọi tập):
- **Mở:** Tavi nói cái máy cần làm gì, đặt ba lô xuống rồi xoay biểu tượng bánh răng ở túi trước. Cuộn bản vẽ trên nóc trải ra, nét sáng xanh ngọc tự vẽ bản vẽ của cái máy đó (chỉ có hình, không có chữ). Nắp bật, dụng cụ và linh kiện bung ra như hoa nở, đúng những thứ trong bản vẽ.
- **Lắp:** ba lô không tự lắp. Tavi lắp bằng tay theo bản vẽ, máy càng to càng lâu.
- **Mỗi lần một máy:** đang có một máy thì ba lô chỉ cho thêm bộ phận của chính máy đó (nắp che nút đỏ, móc ròng rọc ở tập 01). Xoay để lấy máy khác thì chỉ có tiếng PHỤT, hai ống tinh thể nháy hai lần. Xoay ngược biểu tượng thì máy đang có tự tháo ra, mọi linh kiện của ba lô bay về ba lô, đồ không phải của ba lô rơi lại tại chỗ. Tháo xong mới lắp được máy khác.
- **Hay lỗi:** linh kiện đôi khi thiếu hay thừa một món (tập 01 thiếu đúng một bánh răng); lắp sai một chỗ thì máy chạy lệch ý. Lỗi chỉ lộ ra khi chạy thử. Tavi tìm lỗi bằng cách so máy với bản vẽ.
- Máy chạy bằng lõi tinh thể: không dây điện, không ổ cắm, không tia lửa điện.
- Đài thiên văn trên hòn đảo Wonder Hub lóe xanh ngọc thì hai ống tinh thể lóe theo cùng nhịp. Ở EP000B, lần đầu hòn đảo lóe từ khi ba lô ở với Tavi, cuộn bản vẽ còn tự trải ra, phác một cỗ máy khổng lồ rồi chỉ còn hình đài thiên văn. Ngoài lúc đó, ba lô chỉ vẽ cái máy Tavi nói ra. Ba lô không chỉ đường, không báo nguy hiểm.

**Pocket of Wonders hoạt động thế nào** (giữ nguyên mọi tập):
- **Mở:** Piko kéo nút dây có viên đá xanh, miệng túi bung ra, hắt ánh tím nhạt lấp lánh. Miệng túi mở tới khi Piko kéo dây thắt lại (CHÚT); quên thắt thì túi cứ mở.
- **Lấy:** Piko thò một tay vào, rút ra **một món** mỗi lần (PỤP!). Bên trong rộng hơn bên ngoài: món đồ có thể to hơn cái túi nhiều lần, chui ra dần như kéo khăn khỏi mũ ảo thuật.
- **Không kiểm soát được:** món ra là ngẫu nhiên. Piko xin gì cũng không làm túi nghe theo; món ra hiếm khi là thứ Piko đang muốn, nhưng sau đó hay hoá ra có ích theo cách không ngờ. Món lấy ra là đồ thường, không có phép, không tự quay về túi.
- **Đồ rơi vào túi đang mở** thì ở lại trong túi và có thể ra ở một lần rút sau, như mọi món khác (bánh răng vàng: EP000E rơi vào, tập 01 ra cùng con vịt; `03_CONTENT/README.md`).
- Hòn đảo Wonder Hub lóe xanh ngọc thì túi lóe xanh ngọc cùng nhịp. Túi không chỉ đường, không báo nguy hiểm.

## Diễn

Dựng model, rig từng nhân vật (bộ phận nào làm riêng, bộ phận nào chuyển động), bộ ảnh tham chiếu và prompt ChatGPT: `02_ASSET_LIBRARY/MODELING.md`.

**Giới hạn khi diễn:** tay Lumo rất ngắn so với đầu (vai tới cổ tay chỉ 0.22 m), chỉ với tới ngang cằm: không gãi đầu, che mắt, ôm đầu hay vỗ tay trước miệng được; tay giơ cao nhất chỉ tới ngang tai. Động tác ngượng, bối rối dùng nhún vai, xòe tay, cụp tai, nghiêng đầu.

Nori: tay ngắn mọc ở nửa dưới thân tròn (concept T-pose: gốc tay ở khoảng 0.3 chiều cao thân tính từ đáy, tay dài khoảng 0.3 đường kính thân, mắt ở khoảng 0.63), cầm được vật nhỏ bằng một tay, sách nhỏ hay một trang giấy bằng hai tay. Bàn tay trần giơ cao nhất tới dưới mắt: không chạm mặt, mắt, râu sao hay đỉnh đầu, không đưa bàn tay lên ngang mắt; muốn nhìn bàn tay thì xoè trước bụng rồi nghiêng thân nhìn xuống. Đưa Story Lens lên trước mắt bằng cách cầm cán giơ lên (cán bù phần tay thiếu). Không chân: không đứng, không ngồi, dừng thì lơ lửng. Không có túi: Story Lens luôn cầm trong tay, cần hai tay thì đặt kính xuống trước. Cảm xúc dùng cánh (rũ xuống, vỗ nhanh), râu sao (cụp, sáng lóe), nghiêng thân.

Piko (đo trên concept T-pose, chiều cao tính tới chóp sừng là 1): thân thạch hình chuông, rộng khoảng 0.7 ở ngang tay; tay nhỏ mọc hai bên thân ngang miệng (gốc tay ở khoảng 0.48 tính từ đáy, mắt ở khoảng 0.62), dài khoảng 0.19. Hai bàn tay không gặp nhau trước bụng, không với tới miệng, mắt hay sừng. Nghiêng thân sang trái thì tay trái với tới nút dây và miệng Pocket of Wonders ở hông trái. Vật nhỏ cầm bằng một tay bên hông; vật to gần bằng bề ngang thân (gối, giỏ) thì ôm áp vào bụng, hai tay giữ hai bên; đẩy vật nặng bằng cả thân. Ăn bằng cách cúi người cắn món người khác đưa tới hay món đặt trên mặt phẳng, không tung đồ ăn lên đớp. Không chân: nảy, trườn; thân nén, kéo, dẹt ra được rồi phồng lại ngay (rơi xuống chỗ cứng thì dẹt như cái bánh), luôn giữ thể tích. Không bỏ vào miệng thứ gì không phải đồ ăn.

Tay Tavi cũng ngắn, đầu lại rộng hơn hai vai (bộ cutout: vai ở độ cao 0.36, vai tới bàn tay 0.21, kính bảo hộ trên mũ ở khoảng 0.75): tay giơ cao nhất tới ngang mõm, không với tới mắt, kính, mũ hay đỉnh đầu. Gãi cằm được. Kính bảo hộ lên xuống bằng đầu: gật mạnh một cái thì kính trượt từ mũ xuống mắt (CẠCH), hất đầu ra sau thì kính bật lên mũ. Đội lại kính: cầm dây kính ngang ngực, cúi đầu chui vào rồi ngẩng lên. Đồ rơi lên đầu thì lắc đầu cho văng ra.
