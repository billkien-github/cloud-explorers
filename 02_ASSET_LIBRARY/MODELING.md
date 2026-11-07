# Ảnh tham chiếu và model 3D

Ảnh nhân vật, đạo cụ, bối cảnh sinh bằng **ChatGPT**. Mỗi tập chỉ sinh ảnh mà Seedance cần ("Ảnh cho một tập", ảnh và prompt của từng tập ở "Ảnh của từng tập"). Asset nào dựng model thì làm thêm bộ ảnh nhiều góc nhìn ("Bộ ảnh dựng model"), rồi **Blender** dựng lưới, rig, material theo ảnh bằng build script cạnh asset ([`README.md`](README.md)). Hình cuối của shot sinh bằng **Seedance** ([`04_PRODUCTION/SEEDANCE.md`](../04_PRODUCTION/SEEDANCE.md)). Hình dáng, màu, chiều cao nhân vật: [`01_BRAND/Character_Bible/`](../01_BRAND/Character_Bible/README.md); cỡ mọi món: "Bảng cỡ" dưới đây.

Thứ tự trong file: bảng cỡ → quy trình ảnh cho một tập → cách sinh bằng ChatGPT → ảnh của từng tập (theo thứ tự phát hành: Season 0 từ 000A, rồi tập 01) → bộ ảnh dựng model → dựng trong Blender.

## Bảng cỡ

Một món giữ đúng một cỡ ở mọi ảnh, mọi cảnh, mọi tập. Bảng này là nguồn cỡ cho prompt ChatGPT, previz 2D, previz khối, prompt Seedance và model. Kịch bản ghi cỡ của mỗi vật, bối cảnh mới so với nhân vật (`03_CONTENT/README.md`, đoạn "Cỡ"); làm ảnh của tập thì chép vào đây, đổi ra L.

- **Đơn vị L** là chiều cao Lumo. Chiều cao bốn nhân vật chính và nhân vật nền, phụ: Character Bible (Lumo 1, Tavi 0.85, Nori 0.70, Piko 0.80 L).
- **Mốc trên người**, dùng khi kịch bản ghi "ngang ngực", "ngang mắt":
  - Lumo: ngực khoảng 0.38 L (`03_CONTENT/PREVIZ_2D.md`).
  - Tavi: vai 0.36 L (Character Bible), ngực khoảng 0.33 L, hông khoảng 0.2 L.
  - Nori: thân tròn khoảng 0.5 L, tức khoảng 3/4 chiều cao tính tới sao (đo trên `nori_turnaround.png`).
  - Piko: P = 0.8 L, mắt khoảng 0.5 L.
  - Nắm tay Lumo khoảng 0.12 L.
- Dòng ghi "Character Bible" ở cột Theo là cỡ do Character Bible sở hữu, chép vào đây cho đủ một chỗ tra: đổi thì sửa Character Bible trước, rồi sửa dòng đó.
- **Số ghi "ước lượng"** là chưa có trong kịch bản hay ảnh; chốt khi dựng previz rồi sửa bảng. Đo lại trên model khác bảng thì sửa bảng.
- Khoảng cách, bố trí trong một bối cảnh nằm ở beat sheet của tập (góc chợ EP000D: bảng "Bố trí góc chợ").

### Cỡ dùng ở nhiều tập

| Món | Cỡ | Theo |
|---|---|---|
| Lumo, Tavi, Nori, Piko | 1 · 0.85 · 0.70 · 0.80 L | Character Bible |
| Wonder Compass | Lumo cầm một hay hai tay ngang ngực; đường kính khoảng 0.12 L, vừa hốc trên bệ đỡ trống trong `stone_vault_hero.png` | Kịch bản EP000A, ảnh |
| Inventor Pack | Đeo giữa lưng Tavi, dưới hàng gai lớn; cao khoảng 0.27 L (đo trên `tavi_turnaround.png`) | Character Bible, ảnh |
| Story Lens | Nori cầm cán đưa mặt kính lên trước mắt; mặt kính khoảng 0.2 L, bằng nửa bề ngang thân Nori (ước lượng) | Character Bible |
| Pocket of Wonders | Cao khoảng 0.2 L (khoảng 1/4 chiều cao Piko), to hơn quả táo một chút | Character Bible, `piko_turnaround.png` |
| Sinh vật nhỏ của thung lũng | Khoảng 0.17 L (1/6 Lumo) | Character Bible |
| Hòn đảo có Wonder Hub | Chỉ thấy từ xa, nhỏ ở chân trời; cửa chính: bốn hốc ở nửa dưới cửa, trong tầm với của bốn nhân vật | Tập 000A, 000D |

### Cỡ tập 000A

| Món | Cỡ | Theo |
|---|---|---|
| Chú chim nhỏ | Cỡ nắm tay Lumo, khoảng 0.12 L | Character Bible |
| Bướm phát sáng | Cỡ một ngón tay Lumo, sải cánh khoảng 0.05–0.07 L | Character Bible, previz Cảnh 1 |
| Bản đồ giấy | Rộng khoảng 0.36 L, cao 0.3 L (hẹp hơn đầu Lumo một chút); Lumo cầm hai tay ngang ngực | Previz Cảnh 1, take |
| Bệ đá có ngôi sao và bản đồ khắc | Mặt trên ngang ngực Lumo, khoảng 0.38 L | Kịch bản |
| Bệ đỡ trống trong vòm đá | Trụ đá thấp ngang ngực Lumo, khoảng 0.38 L | Kịch bản |
| Cầu ván cổ qua khe núi | Thành cầu có dây leo ngang ngực Lumo, khoảng 0.38 L; mặt cầu rộng cho một người đi, khoảng 0.8 L (ước lượng) | Kịch bản |
| Lối nhỏ bậc đá cạnh cửa | Tay vịn dây leo ngang ngực Lumo; mỗi bậc thấp, Lumo bước lên được, khoảng 0.15 L (ước lượng) | Kịch bản |
| Bụi quả ké (Cảnh 1) | Cao khoảng 1 L, rộng khoảng 0.85 L; quả ké cỡ mũi Lumo, khoảng 0.07 L; lá to hình tim, không gai | Previz Cảnh 1 |
| Hòn đá Lumo vấp | Dài khoảng 0.2 L, nhô khỏi mặt đường khoảng 0.06 L (ngang mắt cá) | Previz Cảnh 1 |
| Vách đá cuối đường (Cảnh 1) | Cao khoảng 4.5 L | Previz Cảnh 1 |
| Sườn dốc lá khô | Thoải; từ đỉnh tới chân cao khoảng 1.3 L | Previz Cảnh 1 |
| Đống lá | Cao khoảng 0.47 L (ngang hông Lumo), rộng khoảng 1.1 L | Previz Cảnh 1 |
| Phiến đá rêu chỗ bướm đậu | Cao khoảng 0.22 L (ngang gối Lumo) | Previz Cảnh 1 |
| Tường phế tích | Cao khoảng 1.42 L, tính cả đá đỉnh tường khoảng 1.5 L | Previz Cảnh 1–2 |
| Phiến đá có ánh vàng | 0.42 × 0.3 L, dày 0.06 L; Lumo ngồi xổm nhấc được | Previz Cảnh 1–2 |
| Ánh vàng dưới phiến đá | Chỉ một viền sáng mỏng khoảng 0.02 L ló ở mép phiến đá, không thấy nguồn; không bao giờ thành vũng sáng | Kịch bản ("le lói"), previz |
| Hòn sỏi, quả gai, chiếc lá | Vật nhỏ cỡ nắm tay Lumo trở xuống; lên hình to hơn cỡ thật (`04_PRODUCTION/SEEDANCE.md`) | Kịch bản |

### Cỡ tập 000B

| Món | Cỡ | Theo |
|---|---|---|
| Máy làm bữa sáng | Cao khoảng 0.85 L (bằng Tavi); núm cần gạt ngang ngực Tavi, khoảng 0.33 L | Prompt |
| Bánh răng nhỏ của máy làm bữa sáng | Cỡ đồng xu, khoảng 0.03 L | Kịch bản |
| Đống linh kiện trong xưởng | Cao ngang ngực Tavi, khoảng 0.33 L | Kịch bản |
| Máy phân loại linh kiện | Cao khoảng 1.7 L (gấp đôi Tavi); miệng phễu và tay quay ngang ngực Tavi, khoảng 0.33 L; miệng ba thùng ngang hông Tavi, khoảng 0.2 L | Kịch bản |
| Cột cần gạt | Cách máy phân loại ba bước; cần gạt ngang ngực Tavi | Kịch bản |
| Cuộn bản vẽ trải ra | Rộng bằng ba lô; trải dọc mặt bậc đá | Kịch bản, prompt |
| Tường đá sân lắp máy | Cao khoảng 1.1 L (cao hơn đầu Tavi, che kín Tavi cả mũ); bậc đá chân tường ngang ngực Tavi, khoảng 0.33 L | Kịch bản |
| Đống phế liệu ở bãi | Không cao quá đầu Tavi, 0.85 L | Beat sheet |
| Thùng gỗ đầy vải vụn | Thành thùng ngang cổ Tavi, khoảng 0.42 L (ước lượng) | Beat sheet |
| Ghế đẩu, bình tưới, xô úp, ấm, chậu hoa | Đồ thường theo cỡ Tavi: ghế cao khoảng 0.3 L; xô úp đủ che con ốc; bình tưới, ấm, chậu khoảng 0.15–0.25 L (ước lượng) | Kịch bản |

### Cỡ tập 000C

| Món | Cỡ | Theo |
|---|---|---|
| Quyển sách nhỏ | Khoảng 0.25 L (nửa thân Nori) | Character Bible |
| Sách bay | 0.1–0.3 L; quyển sách cổ to bự khoảng 0.7 L (cao bằng cả người Nori) | Character Bible |
| Quyển sách bạc | Cao khoảng 0.5 L (bằng thân Nori), dày | Beat sheet |
| Tờ giấy bạc bị thất lạc | Bằng một trang sách bạc, khoảng 0.45 L; gấp tư thì khoảng 0.2 L (ước lượng) | Beat sheet |
| Ba bình hoa | Bình cao nhất khoảng 0.5 L (bằng thân Nori), đủ che quyển sách nhỏ; hai bình kia thấp dần theo `flower_vases_ref.png` | Prompt, ảnh |
| Giá sách | Cao vút, nhiều tầng; giá bảy là giá cao nhất của dãy sách cổ, Nori phải bay lên mới tới | Kịch bản |
| Ô cửa trăng | Ở lưng chừng tường bên; bậu rộng đủ cho quyển sách nhỏ nằm đọc trên đệm | Kịch bản |
| Lan can ban công | Thanh trên phẳng, rộng đủ cho quyển sách nhỏ đậu; cao khoảng 0.5 L (ước lượng) | Kịch bản, prompt |

### Cỡ tập 000D

| Món | Cỡ | Theo |
|---|---|---|
| Bà Gấu bán bánh | Khoảng 1.3 L | Character Bible |
| Cá mây mẹ | Dài khoảng 0.4 L (nửa Piko) | Character Bible |
| Cá mây con | Cỡ quả mận, khoảng 0.05 L (1/8 cá mẹ) | Character Bible |
| Bánh bao mật ong | Cỡ nắm tay Lumo, khoảng 0.12 L | Beat sheet |
| Xửng hấp | Rộng bằng đầu Lumo, khoảng 0.45 L | Prompt |
| Giỏ đan làm tổ | Rộng gần bằng thân Piko, khoảng 0.55 L; treo trên móc ngang mắt Piko, khoảng 0.5 L | Beat sheet |
| Gối bông | Dài bằng Piko, khoảng 0.8 L; dày khoảng 0.4 L (nửa Piko) | Beat sheet |
| Lò xo to | Cao khoảng 0.4 L (nửa Piko), rộng nửa thân Piko | Beat sheet |
| Quầy lều chóp | Chân lều đường kính khoảng 1.2 L (1.5P); mép mái khoảng 0.4 L (0.5P); núm gỗ trên chóp cao khoảng 1.6 L (2P), cỡ nắm tay Lumo | Beat sheet |
| Cột đầu cầu | Cao khoảng 1.2 L (1.5P); móc treo giỏ khoảng 0.5 L (0.6P) | Beat sheet |
| Cầu dây ngắn | Dài khoảng 3.2 L (4P); tay vịn lưới cao khoảng 0.8 L (1P) | Beat sheet |

### Cỡ tập 01

| Món | Cỡ | Theo |
|---|---|---|
| Rain-O-Matic 3000 | Thân (cả chân) cao khoảng 1.1 L, rộng khoảng 1 L; nút đỏ đường kính khoảng 0.2 L, tâm ở 0.4 L (ngang ngực Lumo, khoảng 1/3 chiều cao thân); vòm kính rộng khoảng 0.5 L, ổ bánh răng khoảng 0.07 L; đỉnh giàn ba chân khoảng 1.85 L | Kịch bản, previz Cảnh 2 |
| Nắp che nút đỏ | Rộng khoảng ba lần nút đỏ, khoảng 0.6 L | Prompt, ảnh |
| Bánh răng vàng | Vừa ổ trong vòm kính, mỏ vịt cao su và lòng bàn tay Tavi: khoảng 0.05–0.07 L (previz Cảnh 2: 0.07 L; `rubber_duck_gear.png`: khoảng 0.04 L; chốt khi dựng model) | Prompt, previz, ảnh |
| Móc ròng rọc | Cỡ bàn tay Lumo, lọt qua cửa nhỏ trên vòm kính | Prompt |
| Vịt cao su | Khoảng 0.13 L (1/6 Piko); vật nhỏ nên Piko cầm một tay bên hông (Character Bible, "Giới hạn khi diễn") | Prompt |
| Thìa | Khoảng 0.2 L (1/4 Piko) | Prompt |
| Ô | Tán mở rộng hơn thân Piko một chút, khoảng 0.65 L | Prompt |
| Hộp ốc | Rộng khoảng 0.43 L (nửa chiều cao Tavi) | Prompt |
| Cuộn dây của Noah | Lumo ôm trước bụng bằng hai tay, khoảng 0.3 L | Prompt |
| Con thuyền | To như một quả đồi nhỏ; mạn thuyền cao nhiều lần Lumo, khoảng 4 L (ước lượng) | Prompt |
| Cầu ván | Rộng đủ cho voi con đi, khoảng 0.8 L; tám nẹp cách đều | Prompt |
| Đôi voi con | Con thứ nhất khoảng 1 L; con thứ hai khoảng 0.8 L | Prompt, ảnh `baby_elephants_ref.png` |
| Noah | Khoảng 2.5 L | Prompt |
| Thú trên boong | Thỏ khoảng 0.5 L, chim cỡ chú chim nhỏ, hươu cao cổ ló cổ quá lan can khoảng 1 L (ước lượng) | Prompt |

### Ảnh lệch cỡ so với bảng

Ảnh dưới đây dùng được nhưng cỡ lệch bảng (soát ngày 07/11/2026). Prompt Seedance có ảnh này phải ghi cỡ đúng theo bảng, và ghi trong ACTIVE REFERENCES là không lấy cỡ từ ảnh:

| Ảnh | Lệch | Ghi trong prompt Seedance |
|---|---|---|
| `rain_o_matic_front.png` (và ảnh sau, đóng băng, nắp che) | Giàn ba chân cao khoảng 2.5 L | Đỉnh giàn khoảng 1.85 L, như previz |
| `sorting_machine_ref.png` | Miệng thùng ở khoảng 18% chiều cao máy (khoảng 0.3 L) | Miệng thùng ngang hông Tavi |
| `breakfast_machine_ref.png`, `tavi_workshop_hero.png` | Núm cần gạt ở khoảng nửa chiều cao máy; ghế đẩu khoảng 0.2 L, đống linh kiện khoảng 0.5 L | Núm ngang ngực Tavi; cỡ ghế, đống linh kiện theo bảng |
| `inventor_pack_blueprint.png` | Tờ bản vẽ rộng hơn ba lô | Rộng bằng ba lô, trải dọc mặt bậc đá |
| `flying_books_ref.png` | Quyển nhỏ nhất bằng khoảng 1/2.5 quyển sách cổ to bự | Nhiều quyển nhỏ chỉ bằng 1/5–1/3 quyển to |
| `ark_animals_ref.png` | Chim cao khoảng 2/3 con thỏ | Chim cỡ nắm tay Lumo, bằng 1/4 con thỏ |
| `noah_ark_side.png` | Lan can cao khoảng 1.1 L, che thú trên boong | Lan can ngang ngực Lumo |
| `wonder_hub_island_hero.png` | Hòn đảo chiếm khoảng 1/3 khung | Ở chân trời: khoảng 1/10 bề ngang khung |

## Ảnh cho một tập

Làm khi kịch bản của tập đã chốt qua `/review`, trước previz 2D (các bước của một tập: [`03_CONTENT/README.md`](../03_CONTENT/README.md), mục "Làm một tập"). Chỉ sinh những ảnh Seedance cần để vẽ nhân vật, bối cảnh, đạo cụ giống nhau qua mọi shot; previz 2D và previz khối lấy hình dáng, màu, cỡ từ chính các ảnh này.

1. **Lập danh sách** từ dòng "Asset riêng" trong mục "Sản xuất" của beat sheet, soát lại với kịch bản (thứ kịch bản cần mà beat sheet thiếu thì bổ sung vào beat sheet). Mỗi asset sinh:
   - **Nhân vật phụ:** `<tên>_ref.png` toàn thân nhìn 3/4 và `<tên>_ref_back.png` nhìn sau, ghép thành `<tên>_turnaround.png` bằng `pipeline/turnaround.py` để tải lên Seedance một ảnh mà đủ hai mặt. Nhóm nhân vật nền: một ảnh cả nhóm (`valley_critters_ref.png`).
   - **Địa điểm mới:** một ảnh `<tên>_hero.png`, khổ 16:9, không nhân vật.
   - **Đạo cụ** có thiết kế riêng mà truyện dựa vào (máy Rain-O-Matic, bánh răng vàng): một ảnh `<tên>_ref.png` nhìn 3/4. Thêm ảnh trạng thái chỉ khi trạng thái đó lên hình và khó tả bằng chữ (`_frost`).
   - **Không sinh:** đồ quen thuộc tả được bằng chữ trong prompt Seedance (thìa, ô, cuộn dây), hiệu ứng dựng trong Blender (mây bé), vật nhỏ đã có trong ảnh bối cảnh, thứ đã có ảnh từ tập trước.
2. **Thêm mục "Tập NN"** vào "Ảnh của từng tập", đúng thứ tự phát hành, theo khuôn các tập có sẵn: bảng ảnh trước, mỗi asset một dòng gồm thư mục, tên file ảnh, cột Có để ❌; dưới bảng ghi những thứ không sinh ảnh và vì sao. Tên file theo [`README.md`](README.md).
3. **Viết prompt vào file trước khi sinh:** nhân vật phụ, đạo cụ thành hai mục con "Nhân vật phụ", "Đạo cụ" trong mục "Tập NN", theo thứ tự sinh; bối cảnh ở `04_PRODUCTION/SEEDANCE.md`, mục "Prompt sinh ảnh tham chiếu bằng ChatGPT". Theo khuôn các prompt có sẵn:
   - Đầu mỗi asset ghi vai của nó trong phim (thấy gì, diễn gì), để biết ảnh cần cho thấy những gì.
   - Đính kèm `01_BRAND/Character_Bible/cloud_explorers_character_sheet.png` (bối cảnh: `01_BRAND/Brand_Guideline/world_key_art.png`), ghi rõ chỉ lấy phong cách. Cần so cỡ với nhân vật thì đính kèm thêm `01_BRAND/Character_Bible/cast_lineup.png` (bốn nhân vật cùng đường chân, cao đúng tỉ lệ) và ghi lấy cỡ từ ảnh đó: băng nhóm trên character sheet vẽ Nori, Piko chỉ khoảng nửa Lumo. Các prompt đã có còn ghi "style and scale" với character sheet: sinh lại ảnh nào thì đổi theo luật này.
   - Tả đúng những gì kịch bản cần: bộ phận được dùng tới, đếm được thì ghi số. Nhân vật phụ tránh màu riêng của bốn nhân vật chính.
   - **Cỡ:** mỗi asset có một dòng trong "Bảng cỡ" (thêm dòng trước khi viết prompt, ở mục "Cỡ tập NN", lấy từ kịch bản; kịch bản thiếu cỡ thì bổ sung vào kịch bản trước). Prompt ghi cỡ đúng như bảng, so với nhân vật trong ảnh character sheet đính kèm; ảnh bối cảnh có đặt sẵn đạo cụ hay nhân vật nền thì ghi thêm cỡ của món đó so với đồ quen thuộc đứng cạnh (`about the size of an apple`), vì GPT hay phóng to món quan trọng cho nổi.
   - Nền xám nhạt trơn (trừ ảnh bối cảnh), ánh sáng đều, một đối tượng, không chữ, không logo.
   - Ảnh này đính kèm ảnh kia thì ghi thứ tự làm.
4. **Sinh ảnh:** mỗi asset một chat, mỗi lần một ảnh; cách gửi, tải, lưu và các câu sửa hay dùng ở "Sinh ảnh bằng ChatGPT".
5. **Soát từng ảnh** với Character Bible và kịch bản (số lượng, trạng thái, bên trái bên phải, màu) trước khi gửi prompt kế. Ảnh sau phải cùng cỡ, cùng đường chân với ảnh trước. **Soát cỡ** theo "Bảng cỡ": món đứng cạnh đồ khác hay cạnh bối cảnh (túi giữa giỏ và thùng, bình hoa trên tủ, tường so với cửa xưởng) phải đúng tỉ lệ với nhau và với các ảnh đã có của tập trước; ảnh một món trên nền trơn không cho thấy cỡ, nên cỡ của nó soát ở ảnh bối cảnh có nó và ở previz. Chưa đạt thì nhắn sửa đúng điểm sai trong cùng chat. **Câu sửa nào ăn thì chép vào prompt trong file**, để lần sinh lại không lặp lỗi.
6. **Xong cả tập:** ghép ảnh xoay, đánh ✅ trong bảng, xoá ảnh thừa (bản nháp, ảnh trùng ý), grep để mọi tên file nhắc trong tài liệu đều có thật, cập nhật Trạng thái trong `README.md`. Rồi sang previz 2D.

## Sinh ảnh bằng ChatGPT

- Mỗi chat là một khối có tiêu đề (ảnh của tập: mỗi món in đậm trong mục "Nhân vật phụ", "Đạo cụ" của tập; bộ ảnh dựng model: mỗi mục con của "Prompt dựng model"). Gửi lần lượt từng prompt theo thứ tự, mỗi lần nhận **một ảnh**; ảnh sau và ảnh đủ đồ sinh trong cùng chat với ảnh trước để giữ đúng thiết kế.
- Đính kèm đúng file ghi ở mỗi bước, theo đúng thứ tự khi có nhiều file, kể cả khi ảnh đó đã có sẵn trong chat. Prompt tiếng Anh để GPT giữ đúng từng ý.
- Ảnh T-pose sửa từ ảnh A-pose đã duyệt và chỉ đổi tay. Ảnh sau T-pose sửa từ ảnh sau A-pose, đính kèm thêm ảnh trước T-pose để lấy dáng tay. Nếu để GPT tự vẽ lại T-pose từ đầu, thân hay bị lệch (Tavi từng mất gai hai bên thân, tay to ra và có tay áo).
- Claude làm giúp được qua Claude in Chrome, nhưng phải dùng Chrome trên máy Mac chứa repo: ảnh tải về nằm ở `~/Downloads` của Mac, Claude đổi tên và chuyển vào `concept/`. Chrome trên máy Windows tải về không sang được Mac. Ô chat của ChatGPT gửi tin khi gặp dấu xuống dòng, nên prompt được gõ thành một dòng.
- Lưu ảnh nhận về đúng tên ghi ở mỗi bước vào `concept/` của asset, soát (ảnh cho tập: bước 5 của "Ảnh cho một tập"; ảnh dựng model: thêm "Chuẩn ảnh dựng model") rồi mới gửi bước tiếp; chưa đạt thì nhắn sửa đúng điểm sai trong cùng chat.
- Ảnh sau lệch cỡ, lệch vị trí so với ảnh trước, nhắn: `Same back view, but match the exact size and position of the front image: same top of the head, same feet line, same width.`
- GPT ghép hai góc nhìn vào một ảnh, nhắn: `Only one view per image. Generate it again as a single view.`
- Ảnh sau của vật có chi tiết lệch một bên (Story Lens, mu bàn tay của Noah): GPT hay vẽ lại y như mặt trước. Ghi rõ chi tiết nào chuyển sang bên nào (`the thumb is now on the opposite side`).
- Ảnh nhìn ngang: ghi nhìn từ bên nào và quay về phía nào của người xem (`seen from its left side, facing the viewer's left`), phần chìa ra (tai, cánh) thấy mặt nào. GPT hay vẽ mặt đẹp dù sai góc nhìn (tai voi lộ mặt trong màu hồng). Vật có cơ cấu ở một bên (lò xo, bản lề của nắp che nút): nhìn ngang từ phía có cơ cấu cho khớp ảnh trước.
- Tư thế tham chiếu bỏ đồ nhân vật cầm khi diễn (dây trong vòi voi con); diễn làm sau, ở previz hay rig.
- Ảnh đính kèm để GPT vẽ cho **khác** nó (sách bay khác quyển sách nhỏ): GPT vẫn chép nét riêng của ảnh đó sang (ruy băng đuôi, đai gáy). Ghi rõ từng nét riêng phải bỏ (`NO ribbon bookmarks`).
- GPT hay tự thêm màu, chi tiết không có trong prompt (màu tím trên Rain-O-Matic, cầu dốc ở mạn thuyền): soát với Character Bible và kịch bản, rồi ghi `no …` vào prompt.
- Ghi "a clear gap between the arms and the body" thì GPT có thể vẽ tay rời hẳn khỏi thân (Piko) hoặc đầu tay cắt phẳng, hở một khe với thân như tay búp bê (Nori). Ghi tay mọc liền ở vai (`the shoulder blends into the body, no gap and no flat cut`), chỉ hở giữa mặt dưới cánh tay và thân. Ảnh sửa từ ảnh khác thì GPT hay kéo tay về gần nằm ngang: ghi lại góc (`about 45 degrees below horizontal, an A-pose`). Đổi tư thế tay thì ghi vai giữ nguyên chỗ cũ, nếu không GPT dời vai lên cao (tay T-pose của Nori); ảnh sau thì ghi tay cùng độ cao với ảnh trước (`at exactly the same height on the body as in Image 2`), vì GPT hay đặt tay cao hơn (tay T-pose sau của Piko lệch khoảng nửa bề dày tay). Ảnh sửa từ ảnh khác thì vai có thể đổi kiểu (mọc mềm ở A-pose, nối phẳng ở T-pose): ghi `the shoulder blends smoothly into the body, no flat seam`.
- Sửa cỡ một bộ phận mà giữ thiết kế: đính kèm ảnh cũ, liệt kê đúng những gì đổi, ghi chỗ đặt bằng phần của chiều cao cả vật (`its center at about one third of the height from the ground to the top of the body`). Mỗi lần sửa chỉ đổi một cỡ: sửa cỡ thứ hai thì GPT hay trả lại lỗi của cỡ thứ nhất (Rain-O-Matic: hạ giàn ba chân thì nút đỏ lại lên cao; giữ bản nút thấp, giàn để previz quyết).
- Vật có chi tiết đối xứng (mũi sao tám cánh của Wonder Compass): GPT hay thêm chi tiết mới mà giữ nguyên phần đối xứng cũ. Ghi rõ các phần còn lại phải bằng nhau và vì sao (`not longer than the diagonal ones, it never looks like a fixed compass rose`).
- ChatGPT đôi khi đưa hai bản và hỏi "Which image do you like more?": phải chọn một bản thì mới tải được. Nếu nút tải trong khung xem ảnh không ăn, tải bằng link tạo ngay trong trang (Claude làm được qua công cụ JavaScript của Claude in Chrome).

## Ảnh của từng tập

Mỗi tập: bảng ảnh (sinh theo thứ tự bảng), những thứ không sinh ảnh, rồi prompt nhân vật phụ và đạo cụ. Prompt bối cảnh nằm ở `04_PRODUCTION/SEEDANCE.md`, mục "Prompt sinh ảnh tham chiếu bằng ChatGPT". Cỡ: "Bảng cỡ", mục "Cỡ tập NN".

### Tập 000A

Danh sách asset: beat sheet `03_CONTENT/Scripts/EP000A_mysterious_compass.md`, mục "Sản xuất", đã soát với kịch bản. Sinh theo thứ tự bảng, vì ảnh sau đính kèm ảnh trước. Prompt: nhân vật phụ, đạo cụ ở mục con dưới đây; bối cảnh ở `04_PRODUCTION/SEEDANCE.md`, mục "Prompt sinh ảnh tham chiếu bằng ChatGPT".

| Asset | Thư mục | Ảnh | Có |
|---|---|---|---|
| Chú chim nhỏ | `Characters/Little_Bird/` | `little_bird_ref.png`, `little_bird_ref_back.png`, ghép `little_bird_turnaround.png` | ✅ |
| Bướm phát sáng | `Characters/Glow_Butterflies/` | `glow_butterflies_ref.png` (thiết kế, ba tư thế) | ✅ |
| Bản đồ giấy | `Props/Paper_Map/` | `paper_map_ref.png`; `paper_map_upside_down.png` (xoay 180°, cho đoạn Lumo cầm ngược: Seedance chép chiều của ảnh tham chiếu; không đưa cả hai ảnh vào một lần sinh) | ✅ |
| Rừng Mây | `Environments/Cloud_Forest/` | `cloud_forest_hero.png` | ✅ |
| Phế tích cổ | `Environments/Ancient_Ruins/` | `ancient_ruins_hero.png` | ✅ |
| Vòm đá | `Environments/Ancient_Ruins/` | `stone_vault_hero.png` | ✅ |
| Cầu ván cổ qua khe núi | `Environments/Ancient_Ruins/` | `vine_bridge_hero.png` | ✅ |
| Đỉnh đồi lúc hoàng hôn | `Environments/Sunset_Hill/` | `sunset_hill_hero.png` | ✅ |
| Hòn đảo có Wonder Hub, nhìn từ xa | `Environments/Wonder_Hub/` | `wonder_hub_island_hero.png` | ✅ |
| Bệ đá có ngôi sao và bản đồ khắc | `Props/Star_Plinth/` | `star_plinth_ref.png` | ✅ |
| Bãi phế liệu | `Environments/Junkyard/` | `junkyard_hero.png` | ✅ |

Không sinh ảnh riêng: Lumo, Wonder Compass, Inventor Pack (đã có `lumo_turnaround.png`, `wonder_compass_ref.png`, `inventor_pack_ref.png`); hộp kim loại, bụi gai, sườn dốc lá khô, phiến đá, phù điêu mây (có trong ảnh bối cảnh); cầu sập, phù điêu ánh lên, cửa thấp mở, đài thiên văn lóe xanh ngọc (trạng thái, tả bằng chữ trong prompt Seedance, hình theo previz); hòn sỏi, hòn đá Lumo vấp (Cảnh 1), quả gai, chiếc lá, đống lá (vật nhỏ tả bằng chữ). `wonder_hub_island_hero.png` chốt dáng ngoài của Wonder Hub: ảnh Wonder Hub của tập 01 và các tập sau đính kèm ảnh này.

#### Nhân vật phụ

**Chú chim nhỏ** (nhân vật nền có diễn, Cảnh 1, 4, 5: đậu cành, nghiêng đầu, lấy cánh vỗ bụng cười "CHÍP CHÍP CHÍP", nhảy từng bậc theo sau Lumo, đậu mép bệ đá, gật gù, bay đi; thiết kế: Character Bible, "Nhân vật nền: chú chim nhỏ"). Đính kèm `cloud_explorers_character_sheet.png`, lưu `little_bird_ref.png`, rồi `little_bird_ref_back.png`; ghép `little_bird_turnaround.png` bằng `pipeline/turnaround.py`.
```
The attached sheet shows the four main characters of a soft stylized 3D animated film for young children; use it for style and scale only. Design a tiny forest bird, a background character who watches Lumo the fox, laughs at him by patting its round belly with one wing, hops along behind him and nods.
- Tiny and round: about the size of Lumo's fist. A plump round body, a big round head, a short pointed beak, big shiny dark eyes, short legs with small feet, short rounded wings, a small tuft of feathers on top of the head, and one curly tuft of tail feathers curling up.
- Soft warm brown feathers, a lighter cream-beige belly and two rosy pink cheek spots. No purple, no lavender, no yellow, no aqua or turquoise, no orange.
- Cheerful, cheeky expression, beak closed.
ONE image: full body in a three-quarter view facing the viewer's left, standing on its feet, wings folded at its sides. Centered with some margin, square 1:1. Plain flat light-gray background, soft even lighting, no ground shadow. No text, no logos, no watermark.
```
```
Now the same bird seen from directly behind, as one separate image: same pose, same size and position in the frame, same canvas. The brown back of the head and body, the folded wings and the curly tail tuft are clear; no belly or cheeks visible. Match the exact colors of the front image: the same warm chestnut brown on the head, back and tail, the same darker brown wings with cream-beige feather tips, not more orange or more saturated. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

**Bướm phát sáng** (nhân vật nền Cảnh 1: bay qua các tán cây; một con đậu trên phiến đá trước phế tích, dẫn mắt tới ánh vàng; thiết kế: Character Bible, "Nhân vật nền: bướm phát sáng"). Đính kèm `cloud_explorers_character_sheet.png`, lưu `glow_butterflies_ref.png`.
```
The attached sheet shows the four main characters of a soft stylized 3D animated film for young children; use it for style and scale only. Design a tiny glowing butterfly for a magical cloud forest, a background creature that drifts between the trees and leads the eye.
- Tiny: about the size of one of Lumo the fox's fingers. A small soft round body, two short curled antennae, rounded wings.
- The wings are pale peach-pink and glow softly from within, with a gentle halo of light. No purple, no lavender, no yellow or gold, no aqua or turquoise.
- Simple and cute, never creepy.
A design sheet with the same butterfly in three poses: 1) wings fully open, seen from above; 2) flying, seen from the side; 3) resting with wings folded up, seen from the side. Landscape 16:9 canvas. Plain flat light-gray background, soft even lighting. No text, no labels, no logos, no watermark.
```

#### Đạo cụ

- Mỗi món một chat, lưu ảnh vào `concept/` của thư mục ghi ở bảng "Tập 000A".
- Bản đồ giấy làm đầu tiên; bệ đá làm sau ảnh cầu ván và ảnh hòn đảo (`04_PRODUCTION/SEEDANCE.md`), vì bệ đá đính kèm cả ba.

**Bản đồ giấy** (Cảnh 1, 4, 5: Lumo cầm ngược, xoay qua xoay lại; Cảnh 4 đặt cạnh bản đồ khắc trên bệ đá). Đính kèm `cloud_explorers_character_sheet.png`, lưu `paper_map_ref.png`. Ảnh vẽ bản đồ đúng chiều; cầm ngược là xoay nửa vòng. Soát ảnh bằng cách xoay 180°: mọi hình phải nhìn ra là đang lộn ngược. Ảnh hiện tại chưa đạt: chiếc rương vẽ gần đối xứng nên xoay rồi vẫn trông đứng thẳng, mặt đá dưới các đảo lật lên trông như núi (bản nháp `sh010` Cảnh 1 tập 000A); chỉ mũi tên đọc ra chiều.
```
The attached sheet shows the style of a soft stylized 3D animated film for young children; use it for style and scale only. Design Lumo the fox's homemade treasure map. ONE image: the map lying flat, seen straight from above, orthographic, no perspective, the right way up, isolated.
- A sheet of warm cream parchment with soft worn edges and two faint fold lines (it folds into a small shoulder bag). About as wide as Lumo's head.
- Drawn by hand in brown ink with a few soft colors, simple and readable from far away: five or six small floating islands with tiny round trees, wavy cloud lines between them, a dotted path hopping from island to island.
- One big chunky red arrow in the middle pointing straight DOWN, and right under its tip a small treasure chest, clearly upright: flat bottom, rounded lid on top, gold lock. When the map is turned around, the chest and the arrow must look obviously upside down.
- The right edge of the map is empty cloud sea: wavy cloud lines only, no island there.
- No text, no letters, no numbers, no compass rose, no X mark.
- Square 1:1, centered with some margin. Plain flat light-gray background, soft even lighting, no shadow.
```

**Bệ đá có ngôi sao và bản đồ khắc** (Cảnh 4: Lumo ấn ngôi sao, phiến đá trượt mở, lộ bản đồ khắc ngang ngực Lumo; đài thiên văn khắc lóe xanh ngọc). Đính kèm theo thứ tự `Environments/Ancient_Ruins/concept/vine_bridge_hero.png`, `Props/Paper_Map/concept/paper_map_ref.png`, `Environments/Wonder_Hub/concept/wonder_hub_island_hero.png`; lưu `star_plinth_ref.png`. Ảnh ở trạng thái đã mở; lúc ngôi sao chưa ấn tả bằng chữ trong prompt Seedance.
```
Image 1 shows an old stone plinth on the far side of a vine bridge, Image 2 is Lumo's paper map, Image 3 is a far island with a domed observatory; all from a soft stylized 3D animated film for young children. Create ONE image of the plinth from Image 1 as a separate object, in a three-quarter view from slightly above, isolated, no characters.
- The same weathered stone and moss as in Image 1. A sturdy square plinth whose flat top is at the chest height of Lumo the fox.
- On the top: the raised eight-pointed star from Image 1 in the compass-rose style (four long points alternating with four short points, NOT eight equal points), pressed down level with the surface; next to it a stone slab has slid aside, revealing a carved stone map set into the top.
- The carved map shows the same islands in the same places as Image 2, carved in low relief: islands with tiny round trees and wavy cloud lines; no dotted path, no arrow, no treasure chest. At its right edge, where Image 2 has only empty cloud sea, one extra small island carries a tiny domed observatory with the silhouette of Image 3.
- No text, no letters, no numbers, no religious symbols.
- Square 1:1, centered with some margin. Plain flat light-gray background, soft even lighting, no ground shadow.
```

### Tập 000B

Danh sách asset: beat sheet `03_CONTENT/Scripts/EP000B_impossible_invention.md`, mục "Sản xuất", đã soát với kịch bản. Sinh theo thứ tự bảng, vì ảnh sau đính kèm ảnh trước. Prompt: đạo cụ ở mục con dưới đây (tập không có nhân vật phụ mới); bối cảnh ở `04_PRODUCTION/SEEDANCE.md`, mục "Prompt sinh ảnh tham chiếu bằng ChatGPT".

| Asset | Thư mục | Ảnh | Có |
|---|---|---|---|
| Máy làm bữa sáng | `Props/Breakfast_Machine/` | `breakfast_machine_ref.png` |✅ |
| Xưởng của Tavi, bên trong | `Environments/Tavi_Workshop/` | `tavi_workshop_hero.png` |✅ |
| Sân lắp máy ở bãi phế liệu, ban ngày | `Environments/Junkyard/` | `junkyard_yard_hero.png` |✅ |
| Đảo cối xay gió | `Environments/Windmill_Island/` | `windmill_island_hero.png` |✅ |
| Máy phân loại linh kiện | `Props/Sorting_Machine/` | `sorting_machine_ref.png` |✅ |
| Bản vẽ máy phân loại trên cuộn giấy | `Props/Inventor_Pack/` | `inventor_pack_blueprint.png` |✅ |

Không sinh ảnh riêng: Tavi, Inventor Pack, hộp kim loại, hòn đảo có Wonder Hub (đã có `tavi_turnaround.png`, `inventor_pack_ref.png`, `junkyard_hero.png`, `wonder_hub_island_hero.png`); bãi phế liệu lúc hoàng hôn, mây tách thấy hòn đảo (`junkyard_hero.png`); xưởng lúc hoàng hôn (ánh sáng, tả bằng chữ); bánh răng nhỏ nứt đôi và lành, con ốc, cuộn danh sách, thùng gỗ đầy vải vụn, chiếc tất, ghế đẩu, bình tưới, xô úp, xẻng, ấm, chậu hoa, lát bánh mì, đĩa (đồ quen thuộc, tả bằng chữ, cỡ theo kịch bản); máy phân loại nằm ngang lúc lắp, con mắt quay ra sân, cánh tay duỗi dài, máy tự tháo (trạng thái, hình theo previz); nét phác cỗ máy khổng lồ và hình đài thiên văn trên cuộn giấy (tả bằng chữ theo dáng Chronicle Engine trong `03_CONTENT/README.md`: nhìn từ trên là bốn vòng tròn lồng nhau quanh quả cầu lõi). Post-credit dùng ảnh của tập 000C (`library_interior_hero.png`, `silver_book_ref.png`), sinh ở mục "Tập 000C".

#### Đạo cụ

- Mỗi món một chat, lưu ảnh vào `concept/` của thư mục ghi ở bảng "Tập 000B".
- Máy làm bữa sáng làm trước ảnh xưởng; máy phân loại làm trước ảnh bản vẽ (cả hai ảnh sau đính kèm ảnh trước). Bối cảnh ở `04_PRODUCTION/SEEDANCE.md`.
- Máy của tập này không mang màu riêng của Tavi (xanh lá) và không có ánh xanh ngọc (màu tín hiệu của bảo bối, hòn đảo), trừ nét vẽ trên cuộn bản vẽ.

**Máy làm bữa sáng** (Cảnh 1, 5: Tavi gật cho kính xuống, kéo cần gạt; lõi tinh thể sáng khi chạy, tắt khi dừng; cánh tay phết mứt quay lệch hất mứt lên kính; ống bắn hất lát bánh qua đĩa vào thùng rác; Tavi mở nắp hông lấy bánh răng nhỏ nứt đôi; phiên bản 28: bệ lò xo dưới đĩa hất lát bánh dính trần). Đính kèm `cloud_explorers_character_sheet.png`, lưu `breakfast_machine_ref.png`. Ảnh ở trạng thái dừng, lõi tắt; lúc chạy tả bằng chữ.
```
The attached sheet shows the characters of a soft stylized 3D animated film for young children; use it for style and scale only. Design the homemade breakfast machine of Tavi, the small green lizard inventor in the sheet. ONE image: the machine in a three-quarter view, isolated, no characters.
- A chubby round machine about as tall as Tavi, made of warm copper and brass with rivets, soft rounded shapes, a little patched but cute.
- In the middle of its body, behind a small round glass window: a small amber crystal core, dim (the machine is switched off). No wires, no plugs, no cables, no fire, no heating coils, no toaster slots.
- On the front, a slot with one slice of bread sticking out a little. On the left side, a jointed mechanical arm holding a flat spreading spoon with a dab of red jam. On top, a short launch tube pointing up.
- On the right side, a closed round side hatch with a small latch. Next to it, a lever on the machine with a round knob at Tavi's chest height.
- On the floor beside the machine: a plain round plate resting on a small round spring platform.
- No green, no aqua or turquoise, no purple. No text, no letters, no numbers.
- Square 1:1, centered with some margin. Plain flat light-gray background, soft even lighting, no ground shadow.
```

**Máy phân loại linh kiện** (Cảnh 3–4: lắp từ linh kiện của Inventor Pack; đồ đổ vào phễu, băng chuyền đưa qua dưới con mắt, cánh tay gắp bỏ vào đúng thùng; con mắt lỏng cổ quay ra sân, cánh tay duỗi dài gắp kính, ghế, Tavi; tự tháo bay về ba lô). Đính kèm theo thứ tự `cloud_explorers_character_sheet.png`, `Props/Inventor_Pack/concept/inventor_pack_ref.png`; lưu `sorting_machine_ref.png`. Ảnh ở trạng thái đủ ốc, con mắt nhìn xuống băng chuyền; lỗ ốc trống, con mắt quay ra sân, máy nằm ngang lúc lắp tả bằng chữ, hình theo previz.
```
Image 1 shows the characters of a soft stylized 3D animated film for young children, for style and scale only. Image 2 is Tavi's backpack; the parts of this machine come out of it, so use the same warm brass, copper and brown leather look. Design the parts sorting machine that Tavi (the small green lizard in Image 1) builds. ONE image: the machine in a three-quarter view from the front, slightly above, isolated, no characters.
- Twice as tall as Tavi. A sturdy frame of brass and copper with rivets, soft rounded shapes, friendly and a little clunky. The height comes from a slim tower at the back that carries the eye high up; everything Tavi uses stays LOW.
- At the low end, a wide funnel whose rim is at Tavi's chest height: only one fifth of the machine's height. From the funnel a long conveyor belt runs diagonally up to the top of the tower.
- At the top, on a swivel neck, one big round glass lens looking down at the belt: a smooth clear round lens, no eyelids, no eyebrows, no red glow, never creepy. One clearly visible bolt holds the neck.
- On one side, a jointed grabbing arm folded neatly, ending in a soft rounded three-finger claw.
- In front of the machine, three low open bins in a row, their rims at Tavi's hip height: only one eighth of the machine's height. Each bin has one simple picture painted on its side: a screw, a gear, a spring. No text.
- At the foot of the frame, a hand crank at Tavi's chest height, level with the funnel rim.
- Three steps away from the machine, clearly apart from it, a wooden post with a lever on top, the post as tall as the funnel rim.
- No green, no aqua or turquoise, no purple. No text, no letters, no numbers.
- Square 1:1, centered with some margin. Plain flat light-gray background, soft even lighting, no ground shadow.
```

**Bản vẽ máy phân loại trên cuộn giấy** (Cảnh 2: ba lô tự vẽ bản vẽ; Cảnh 3–4: bản vẽ trải trên bậc đá, Tavi so máy với bản vẽ, thấy con ốc ở cổ con mắt). Đính kèm theo thứ tự `Props/Inventor_Pack/concept/inventor_pack_ref.png`, `Props/Sorting_Machine/concept/sorting_machine_ref.png`; lưu `inventor_pack_blueprint.png`.
```
Image 1 is Tavi's backpack, Image 2 is a parts sorting machine; both from a soft stylized 3D animated film for young children. Create ONE image of the same backpack from Image 1 standing on the ground in a three-quarter view, isolated, no characters. The blue paper scroll on top of the backpack has unrolled forward and lies long and FLAT on the ground in front of it like a rug, as wide as the backpack, seen from slightly above so the drawing is easy to read; it does not stand up.
- On the scroll, a simple glowing aqua line drawing of the machine from Image 2, seen from the side: the funnel at the low end, the diagonal belt, the round lens on its neck with one bolt clearly drawn on the neck, the grabbing arm, the three bins with a screw, a gear and a spring pictured on them, the hand crank at the foot, a lever on a post a little apart, and beside the machine a small heap of odd junk.
- Lines only, like a glowing sketch on blue paper. No text, no letters, no numbers, no labels, no arrows.
- The backpack keeps exactly the design of Image 1; its two crystal tubes glow softly aqua.
- Wide 16:9, centered with some margin. Plain flat light-gray background, soft even lighting, no ground shadow.
```

### Tập 000C

Danh sách asset: beat sheet `03_CONTENT/Scripts/EP000C_forgotten_story.md`, mục "Sản xuất", đã soát với kịch bản. Sinh theo thứ tự bảng, vì ảnh sau đính kèm ảnh trước. Prompt: nhân vật phụ, đạo cụ ở mục con dưới đây; bối cảnh ở `04_PRODUCTION/SEEDANCE.md`, mục "Prompt sinh ảnh tham chiếu bằng ChatGPT". Ảnh thư viện, sách giữ đúng ràng buộc "không mang dáng nơi thờ tự" ở mục "Sản xuất" của beat sheet.

| Asset | Thư mục | Ảnh | Có |
|---|---|---|---|
| Thư viện cổ, nhìn từ ngoài | `Environments/Library/` | `library_exterior_hero.png` |✅ |
| Ba bình hoa | `Props/Flower_Vases/` | `flower_vases_ref.png` |✅ |
| Trong thư viện | `Environments/Library/` | `library_interior_hero.png` |✅ |
| Ban công thư viện lúc hoàng hôn | `Environments/Library/` | `library_balcony_hero.png` |✅ |
| Quyển sách bạc | `Props/Silver_Book/` | `silver_book_ref.png` (đóng); `silver_book_open.png` (mở, trang trắng, khe thiếu trang); `silver_book_symbols.png` (trang bốn biểu tượng) |✅ |
| Quyển sách nhỏ | `Characters/Little_Book/` | `little_book_ref.png`, `little_book_ref_back.png`, ghép `little_book_turnaround.png` |✅ |
| Sách bay | `Characters/Flying_Books/` | `flying_books_ref.png` (cả đàn, có quyển sách cổ to bự) |✅ |
| Khu chợ nổi lúc hoàng hôn | `Environments/Floating_Market/` | `floating_market_hero.png` |✅ |

Không sinh ảnh riêng: Nori, Story Lens, Pocket of Wonders, hòn đảo có Wonder Hub (đã có `nori_turnaround.png`, `story_lens_ref.png`, `pocket_of_wonders_ref.png`, `wonder_hub_island_hero.png`); tờ giấy bạc gấp tư và mở ra (cùng chất với mép trang sách bạc, tả bằng chữ); hốc chứa kính trong ruột sách bạc, trang sách tự lật có hình chuyển động (trạng thái, tả bằng chữ, hình theo previz); hình trong mặt kính (vầng trăng, bình hoa, trang bạc, cánh cửa tròn bốn hốc: làm bằng shader, tả bằng chữ); cuốn truyện phiêu lưu, đệm trên bậu, cánh hoa (vật nhỏ, tả bằng chữ); vệt nắng và luồng nắng (ánh sáng của ảnh trong thư viện, Blender). Khu chợ nổi là bối cảnh chính của EP000D, chốt dáng ở ảnh này (`03_CONTENT/README.md`, mục Season 0).

#### Nhân vật phụ

**Quyển sách nhỏ** (nhân vật nền có diễn cả tập: chúi mắt đọc trên bậu, vụt đi trốn, gập bìa BỘP, ló ra rồi nằm im, giũ trang xoay tròn, đậu lan can; thiết kế: Character Bible, "Nhân vật nền: quyển sách nhỏ"). Đính kèm `cloud_explorers_character_sheet.png`, lưu `little_book_ref.png`, rồi `little_book_ref_back.png`; ghép `little_book_turnaround.png` bằng `pipeline/turnaround.py`. Trang giấy bạc kẹp bên trong là trạng thái, không vẽ vào ảnh này.
```
The attached sheet shows the four main characters of a soft stylized 3D animated film for young children; use it for style and scale only. Design the Little Book, a living storybook that loves adventure stories and sneaks off to read them; a background character that never speaks and acts only with its covers, pages and ribbon.
- About half the size of Nori's round body (the small lavender light spirit in the sheet). A small, thick hardcover book: dark brick-red cloth covers, the spine and the four corners bound in dark brown leather, warm cream pages.
- Two big round friendly eyes on the front cover. No mouth, no arms, no legs: it flies by flapping its two covers like wings.
- A cream ribbon bookmark sticks out of the bottom of the pages and curls like a little tail.
- Nothing tucked between its pages. No text, no title, no letters on the cover or spine.
ONE image: the book upright and closed, floating a little, in a three-quarter view facing the viewer's left, eyes curious and happy. Centered with some margin, square 1:1. Plain flat light-gray background, soft even lighting, no ground shadow. No logos, no watermark.
```
```
Now the same book seen from directly behind, as one separate image: same pose, same size and position in the frame, same canvas. The back cover in the same dark brick-red cloth with dark brown leather corners, no eyes on this side; the leather spine and the cream ribbon tail are clear. Match the exact colors of the front image. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

**Sách bay** (nhân vật nền: bay như đàn chim giữa các giá, một quyển bay tới khi được gọi, cả đàn ập xuống vùi Nori; quyển sách cổ to bự bay chậm, chao đảo, rơi trúng đầu Nori; thiết kế: Character Bible, "Nhân vật nền: sách bay"). Đính kèm theo thứ tự `cloud_explorers_character_sheet.png`, `Characters/Little_Book/concept/little_book_ref.png`; lưu `flying_books_ref.png`.
```
Image 1 shows the characters of a soft stylized 3D animated film for young children, for style and scale only. Image 2 is the Little Book, a living book with eyes; the books in this image must look clearly different from it. Design the flying books of an old magic library: background characters that fly between the shelves like a flock of birds, flapping their covers like wings.
- Ordinary old hardcover books with NO faces and no eyes, in many sizes, with muted covers: brown, cream, light brick red, and a neutral warm gray (not blue). Simple worn covers with plain borders; plain smooth spines without raised leather bands; NO ribbon bookmarks (the ribbon tail belongs only to the Little Book of Image 2); no moons, no stars, no symbols, no text.
- One of them is a very big, thick old book with a heavy brown cover and brass corners (the only book with metal corners), about as tall as Nori's whole body (the small lavender light spirit in Image 1), flying slowly and a little wobbly.
- Calm and graceful, never scary, never competing with the main characters.
A design sheet: about six books in different flying poses (covers spread like wings, mid-flap, gliding), plus the big old book. Landscape 16:9 canvas. Plain flat light-gray background, soft even lighting. No text, no labels, no logos, no watermark.
```

#### Đạo cụ

- Mỗi món một chat, lưu ảnh vào `concept/` của thư mục ghi ở bảng "Tập 000C".
- Ba bình hoa làm trước ảnh trong thư viện (`04_PRODUCTION/SEEDANCE.md`), vì ảnh đó đính kèm ảnh bình hoa.

**Ba bình hoa** (Cảnh 1: quyển sách nhỏ trốn sau bình ba bông; Cảnh 3: hình trong kính là bình ba bông, Nori đếm hoa chọn đúng bình, sau bình có một cánh hoa rơi). Đính kèm `cloud_explorers_character_sheet.png`, lưu `flower_vases_ref.png`.
```
The attached sheet shows the characters of a soft stylized 3D animated film for young children; use it for style and scale only. Design three flower vases that stand on a low cabinet in the corner of an old library. ONE image: the three vases side by side, seen from the front at eye level, isolated, no cabinet, no characters.
- Three different vases with different shapes and heights, in soft muted ceramic colors (cream, sage green, dusty blue); no purple, no lavender, no orange.
- From left to right: a small round vase with exactly ONE flower, a medium vase with exactly TWO flowers, the tallest vase with exactly THREE flowers. All flowers are the same simple kind (soft pink round blossoms on green stems), so only the count tells the vases apart, and the count is easy to read from far away.
- The tallest vase is about as tall as Nori's round body (the small lavender light spirit in the sheet) and wide enough for a small book half Nori's size to hide behind it.
- No text, no letters, no numbers. Wide 3:2, centered with some margin. Plain flat light-gray background, soft even lighting, no ground shadow.
```

**Quyển sách bạc** (Cảnh 1: bị ép bật khỏi giá, lượn xuống bàn đọc, bật mở trang trắng, mép trang ánh bạc, khe thiếu trang ở gáy; Cảnh 2: hốc giữa sách chứa Story Lens; Cảnh 4: đủ trang thì tự lật, dừng ở trang bốn biểu tượng). Đính kèm `cloud_explorers_character_sheet.png`, lưu `silver_book_ref.png`, rồi `silver_book_open.png`. Ảnh thứ ba đính kèm theo thứ tự `silver_book_open.png`, `Environments/Wonder_Hub/concept/wonder_hub_island_hero.png`, `Props/Star_Plinth/concept/star_plinth_ref.png`, `Props/Story_Lens/concept/story_lens_ref.png`, `Props/Pocket_of_Wonders/concept/pocket_of_wonders_ref.png`; lưu `silver_book_symbols.png`. Bốn biểu tượng theo `03_CONTENT/README.md`, mục Season 0.
```
The attached sheet shows the characters of a soft stylized 3D animated film for young children; use it for style and scale only. Design the Silver Book, a magic old book that has lost its story. ONE image: the book closed, standing upright, in a three-quarter view, isolated, no characters.
- As tall as Nori's round body (the small lavender light spirit in the sheet), and thick. A hardcover of neutral cool brushed silver, like real silver metal (no lavender, purple or pink tint anywhere, including the page edges and highlights), with a faint engraved border of small clouds around the front cover, rounded corners.
- The page edges are gilded silver and shimmer.
- No moon, no stars, no symbols on the cover. No text, no letters, no title.
- Square 1:1, centered with some margin. Plain flat light-gray background, soft even lighting, no ground shadow.
```
```
Now the same book lying open flat on its back, seen from above at a slight angle, same scale, as one separate image. The outer edges of both covers are plain smooth rounded edges; the spine with its raised bands is only in the middle, under the missing-page slot. The cover stays the same neutral silver. Both open pages are completely blank warm white paper, no drawings, no text; the page edges shimmer silver. In the spine between the two pages, a thin gap where one page is missing: a narrow slot with silver-shimmering edges, clearly visible. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
```
Image 1 is the open Silver Book from this chat. Image 2 is a far island with a domed observatory, Image 3 a stone plinth with a compass-rose star, Image 4 a hand lens, Image 5 a small pouch. Create the same open book, same view and scale, as one separate image, now complete (no gap in the spine) and open on its last picture page, drawn like a simple children's picture book in soft colored pencil on the warm white paper:
- Right page, in the middle: the domed observatory of Image 2 as a simple drawing. Around it, in a ring, four simple symbols evenly spaced, each about the size of the dome: the eight-pointed star of Image 3 in the compass-rose style (four long points alternating with four short points, NOT eight equal points); a simple gear with eight rounded teeth; a round hand lens with a handle like Image 4; a small pouch tied at the top like Image 5.
- The star, the gear and the hand lens glow softly warm gold from within the paper. The pouch is drawn in dark gray and does not glow.
- Left page: a simple drawing of floating islands in a cloud sea.
- No moon anywhere. No text, no letters, no numbers. Plain flat light-gray background, soft even lighting, no ground shadow.
```

### Tập 000D

Danh sách asset: beat sheet `03_CONTENT/Scripts/EP000D_magic_pocket.md`, mục "Sản xuất" và bảng "Bố trí góc chợ", đã soát với kịch bản. Sinh theo thứ tự bảng, vì ảnh sau đính kèm ảnh trước. Prompt: nhân vật phụ, đạo cụ ở mục con dưới đây; bối cảnh ở `04_PRODUCTION/SEEDANCE.md`, mục "Prompt sinh ảnh tham chiếu bằng ChatGPT". Cỡ trong prompt lấy từ bảng "Bố trí góc chợ", tính theo chiều cao Piko (P = 0.8 Lumo).

| Asset | Thư mục | Ảnh | Có |
|---|---|---|---|
| Bà Gấu bán bánh | `Characters/Granny_Bear/` | `granny_bear_ref.png`, `granny_bear_ref_back.png`, ghép `granny_bear_turnaround.png` | ❌ |
| Cá mây mẹ | `Characters/Cloud_Fish/` | `cloud_fish_ref.png`, `cloud_fish_ref_back.png`, ghép `cloud_fish_turnaround.png` | ❌ |
| Cá mây mẹ và ba cá con | `Characters/Cloud_Fish/` | `cloud_fish_family_ref.png` | ❌ |
| Xửng hấp trên viên đá tinh thể, có bánh bao mật ong | `Props/Bun_Steamer/` | `bun_steamer_ref.png` | ❌ |
| Giỏ đan làm tổ | `Props/Nest_Basket/` | `nest_basket_ref.png` | ❌ |
| Gối bông | `Props/Pillow/` | `pillow_ref.png` | ❌ |
| Lò xo to | `Props/Spring/` | `spring_ref.png` | ❌ |
| Quầy lều chóp | `Environments/Floating_Market/` | `tent_stall_ref.png` | ❌ |
| Đảo quầy bánh, buổi sáng | `Environments/Floating_Market/` | `floating_market_bakery_hero.png` | ❌ |
| Góc chợ yên tĩnh, buổi sáng | `Environments/Floating_Market/` | `floating_market_corner_hero.png` | ❌ |
| Cửa chính Wonder Hub, ban đêm | `Environments/Wonder_Hub/` | `wonder_hub_door_hero.png` | ❌ |

Không sinh ảnh riêng: Piko, Pocket of Wonders, hòn đảo có Wonder Hub (đã có `piko_turnaround.png`, `pocket_of_wonders_ref.png`, `wonder_hub_island_hero.png`); mép chợ lúc hoàng hôn và cây cầu dài hướng ra chân trời (`floating_market_hero.png`); cảnh toàn chợ buổi sáng ở Cảnh 1 (tả bằng chữ theo hai ảnh buổi sáng); bánh bao mật ong (có trong `bun_steamer_ref.png`); quả tròn, cuộn vải đỏ, chuông gió, chồng rổ, dãy vải phơi, khay, rổ, thùng (đồ quen thuộc, có trong ảnh bối cảnh); làn hơi thơm, giọt nước, ánh tím của túi, ánh lóe xanh ngọc (hiệu ứng); Piko dẹt, Piko cuộn trong vải, giỏ treo nghiêng trên núm, gối gập, lò xo nằm nghiêng, bốn hốc cửa lóe (trạng thái, tả bằng chữ, hình theo previz). Cá con trong giỏ là trạng thái: khi sinh Seedance tải lên cả `cloud_fish_family_ref.png` và `nest_basket_ref.png`. Ảnh góc chợ cố ý không có giỏ, túi, gối, lò xo, vì các món này đổi chỗ trong tập; mỗi món tải lên ảnh riêng. `wonder_hub_door_hero.png` chốt cửa chính cho EP000E: bốn hốc theo đúng hình và vị trí trên trang `silver_book_symbols.png`, nằm ở nửa dưới cửa cho bốn nhân vật với tới; cửa chia bốn múi như cánh quạt, mỗi múi một hốc (độ cao từng hốc: beat sheet EP000E, mục "Bố trí").

#### Nhân vật phụ

**Bà Gấu bán bánh** (nhân vật phụ, Cảnh 1, 3, 5: mở nắp xửng, nhấc bánh, cầm bánh đưa tới trước miệng Piko; giơ vạt tạp dề hứng quả; bưng khay bánh qua cầu, đặt bánh vào giỏ cá; gỡ cuộn vải; nói chậm, hay cười; thiết kế: Character Bible, "Nhân vật phụ: bà Gấu bán bánh"). Đính kèm `cloud_explorers_character_sheet.png`, lưu `granny_bear_ref.png`, rồi `granny_bear_ref_back.png`; ghép `granny_bear_turnaround.png` bằng `pipeline/turnaround.py`.
```
The attached sheet shows the four main characters of a soft stylized 3D animated film for young children; use it for style and scale only. Design Granny Bear, a kind old bear who sells honey buns at a floating market; a supporting character who speaks slowly, smiles a lot, hands buns to customers and catches rolling fruit in her apron.
- About 1.3 times as tall as Lumo the fox. A round, soft, plump bear with a big round head in the same chibi proportions as the sheet, small round ears, a gentle smile, small kind dark eyes.
- Soft milky cocoa-brown fur, not orange, not reddish; a cream muzzle and a cream belly patch.
- A cream apron tied at the back, with one big pocket on the front; the apron hem is long enough for her to lift it with both paws like a basket.
- Arms long enough to hold a tray in front of her and to hand a bun forward with one paw.
- No orange, no green, no purple, no turquoise anywhere. No glasses, no hat, no jewelry.
ONE image: full body in a three-quarter view facing the viewer's left, standing in a relaxed pose, arms slightly away from the body, paws empty. Centered with some margin, square 1:1. Plain flat light-gray background, soft even lighting, no ground shadow. No text, no logos, no watermark.
```
```
Now the same bear seen from directly behind, as one separate image: same pose, same size and position in the frame, same canvas. The back of the head and ears, the milky cocoa-brown fur of the back, a short round tail and the apron strings tied in a bow at the back are clear; no face, no muzzle, no apron pocket visible. Match the exact colors of the front image. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

**Cá mây mẹ** (nhân vật nền có diễn gần như cả tập: ló lên sau mái quầy, ngoạm bánh, ngậm bánh bơi lượn giữa các quầy như bơi trong nước, đậu trên núm chóp lều, ngậm quai giỏ quẫy vây, lượn quanh Piko, vẫy đuôi rối rít; thiết kế: Character Bible, "Nhân vật nền: cá mây"). Đính kèm `cloud_explorers_character_sheet.png`, lưu `cloud_fish_ref.png`, rồi `cloud_fish_ref_back.png`; ghép `cloud_fish_turnaround.png` bằng `pipeline/turnaround.py`.
```
The attached sheet shows the four main characters of a soft stylized 3D animated film for young children; use it for style and scale only. Design a cloud fish, a small fish that swims through the air above a sea of clouds as if it were water; a background character who never speaks, only chirps, and carries food home to her babies in her mouth.
- Body length half of Piko's height (Piko: the small clear blue jelly with two dark blue horns in the sheet). A round, plump body, big round shiny eyes, two small rosy pink cheek dots, a small mouth that can open wide enough to carry a bun the size of Lumo the fox's fist.
- Ivory-white body with only a soft warm pearly sheen; fins and a flowing tail thin and translucent like chiffon, ivory with a faint warm pink edge.
- No hands, no arms, no legs. No water, no bubbles.
- No turquoise, no aqua, no blue, no purple or lavender, no yellow, no rainbow iridescence.
- Cute and gentle, never scary, mouth closed.
ONE image: full body in a three-quarter view facing the viewer's left, swimming level in the air, fins spread. Centered with some margin, square 1:1. Plain flat light-gray background, soft even lighting, no ground shadow. No text, no logos, no watermark.
```
```
Now the same fish seen from directly behind, as one separate image: same pose, same size and position in the frame, same canvas. The flowing chiffon tail faces us, the back of the round body and the spread side fins are clear; the eyes only peek out at the sides, no face. Match the exact colors of the front image: ivory with a soft warm pearly sheen, no blue, no purple. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

**Cá mây mẹ và ba cá con** (Cảnh 1–5: ba cá con ló đầu khỏi giỏ, há miệng PIP, bám mép giỏ, nép sát Piko, cùng đẩy mẩu bánh ra; chưa bơi xa được). Gửi trong cùng chat với cá mẹ, sau ảnh nhìn sau; lưu `cloud_fish_family_ref.png`.
```
Now one separate image of the same mother fish with her three babies, to show their size and look. Landscape 16:9 canvas. The mother on the left in the same three-quarter view; next to her, floating in a little row, three baby cloud fish, each about the size of a plum, about one eighth of the mother's length, with the same ivory body, pearly sheen, chiffon fins and pink cheeks, but rounder, with even bigger eyes and tiny stubby fins. The three babies look alike; one has its mouth open as if chirping. No basket, no water, no bubbles. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

#### Đạo cụ

- Mỗi món một chat, lưu ảnh vào `concept/` của thư mục ghi ở bảng "Tập 000D".
- Cá mây (mục trên) làm trước giỏ tổ; xửng hấp làm trước ảnh đảo quầy bánh, quầy lều chóp trước ảnh góc chợ (`04_PRODUCTION/SEEDANCE.md`), vì ảnh sau đính kèm ảnh trước.

**Xửng hấp trên viên đá tinh thể** (Cảnh 1: bà Gấu mở nắp, nhấc ra chiếc bánh bao mật ong cuối cùng, khay trống; Cảnh 5A: mẻ mới, hơi bốc nghi ngút). Đính kèm `cloud_explorers_character_sheet.png`, lưu `bun_steamer_ref.png`.
```
The attached sheet shows the characters of a soft stylized 3D animated film for young children; use it for style and scale only. Design a magical bun steamer for the bakery stall of a kind bear in a floating market. ONE image: the steamer on its crystal, in a three-quarter view from slightly above, isolated, no counter, no characters.
- A round bamboo steamer basket with a woven bamboo lid, about as wide as Lumo the fox's head. The lid is lifted and leans against its side, so we see inside.
- Inside: exactly ONE honey bun, the last one: a soft round steamed bun the size of Lumo's fist, glazed shiny golden with honey. The rest of the steamer is empty.
- The steamer sits on a smooth rounded crystal stone that glows warm amber from within, held in a small low wooden cradle. A few soft wisps of white steam rise. No fire, no flames, no coals, no stove, no smoke.
- No text, no logos. Square 1:1, centered with some margin. Plain flat light-gray background, soft even lighting, no ground shadow.
```

**Giỏ đan làm tổ** (Cảnh 1–5: treo trên móc ở cột đầu cầu, ngang mắt Piko, ba cá con ló ra; Cảnh 3: bật khỏi móc, quai mắc vào núm gỗ trên chóp lều, treo nghiêng; Cảnh 4: Piko ôm giỏ áp vào bụng, trượt xuống mái, treo lại vào móc). Đính kèm theo thứ tự `cloud_explorers_character_sheet.png`, `Characters/Cloud_Fish/concept/cloud_fish_family_ref.png`; lưu `nest_basket_ref.png`. Ảnh giỏ trống; cá con, bánh trong giỏ là trạng thái.
```
Image 1 shows the characters of a soft stylized 3D animated film for young children, for style and scale only. Image 2 shows a family of small cloud fish, for scale only; do not draw them. Design an old woven basket that the cloud fish use as their nest. ONE image: the empty basket in a three-quarter view from slightly above, isolated, no hook, no fish, no characters.
- A round, fairly deep wicker basket of soft honey-brown woven reeds, a little old and worn (a few loose strands), about as wide as Piko's body (the small clear blue jelly with two dark blue horns in Image 1), deep enough to hold the three tiny fish of Image 2 and a bun the size of Lumo the fox's fist.
- One sturdy arched handle of braided reed over the top, from one side of the rim to the other, big enough to hang on a hook or catch on a round knob.
- A soft folded cream cloth lines the bottom. Nothing else inside.
- No text, no logos. Square 1:1, centered with some margin. Plain flat light-gray background, soft even lighting, no ground shadow.
```

**Gối bông** (Cảnh 2: lần rút đầu tiên, chui ra khỏi túi, nằm trên ván; Cảnh 4: Piko đẩy tới sát mép mái lều, gối gập đôi kẹp Piko, rồi đỡ Piko và cái giỏ, lõm sâu rồi phồng lại; gối không có phép). Đính kèm `cloud_explorers_character_sheet.png`, lưu `pillow_ref.png`.
```
The attached sheet shows the characters of a soft stylized 3D animated film for young children; use it for style and scale only. Design a big ordinary pillow that comes out of a magic pouch. ONE image: the pillow lying flat, in a three-quarter view from slightly above, isolated, no characters.
- A big, very soft, plump cotton pillow: as long as Piko is tall (Piko: the small clear blue jelly with two dark blue horns in the sheet), and lying flat about half as thick as Piko is tall. Rectangular with soft rounded corners, puffy and squishy-looking.
- Plain white cotton with a fine stitched seam along the edges. No pattern, no buttons, no lace, no tassels, no colors.
- An ordinary pillow, nothing magical: no glow, no sparkles.
- No text, no logos. Square 1:1, centered with some margin. Plain flat light-gray background, soft even lighting, no ground shadow.
```

**Lò xo to** (Cảnh 2: lần rút thứ hai, nảy tưng tưng trên ván, Piko dựng đứng lên, ngồi phịch thì bắn vọt; Cảnh 3–4: đổ nghiêng, gió lăn lộc cộc, va chân cột BOING; Cảnh 4: ngồi khẽ nảy thấp, ngồi vừa lên đúng tầm chóp lều; lò xo không có phép). Đính kèm `cloud_explorers_character_sheet.png`, lưu `spring_ref.png`. Ảnh dựng đứng; nằm nghiêng tả bằng chữ.
```
The attached sheet shows the characters of a soft stylized 3D animated film for young children; use it for style and scale only. Design a big ordinary coil spring that comes out of a magic pouch. ONE image: the spring standing upright, in a three-quarter view from slightly above, isolated, no characters.
- A chunky metal coil spring, half as tall as Piko (the small clear blue jelly with two dark blue horns in the sheet) and about half as wide as Piko's body, so Piko can sit on top of it. Thick round wire, about eight coils, evenly spaced and springy-looking.
- Both ends are flat closed coils, so it stands steadily and can also lie on its side and roll.
- Soft brushed steel gray with a gentle shine, cartoon-simple. No sharp ends, no rust. No top plate, no seat, no base.
- An ordinary spring, nothing magical: no glow.
- No text, no logos. Square 1:1, centered with some margin. Plain flat light-gray background, soft even lighting, no ground shadow.
```

**Quầy lều chóp** (Cảnh 2: cá mẹ đậu trên núm gỗ, Piko nảy không tới, trườn lên nửa mái thì tuột; Cảnh 3: quai giỏ mắc vào núm; Cảnh 4: Piko bật lò xo lên, dẹt thân ôm quanh chóp, ôm giỏ trượt xuống mái như cầu tuột, lăn vào gối ở mép mái). Số đo theo bảng "Bố trí góc chợ" của beat sheet: chân lều đường kính 1.5P, núm cao 2P, mép mái 0.5P. Đính kèm theo thứ tự `Environments/Floating_Market/concept/floating_market_hero.png`, `cloud_explorers_character_sheet.png`; lưu `tent_stall_ref.png`.
```
Image 1 is a floating market from a soft stylized 3D animated film for young children; Image 2 shows the characters, for scale only. Design ONE special stall for this market, the tallest stall of its quiet corner: a round tent stall with a cone roof. ONE image: the whole stall in a three-quarter view at eye level, isolated, standing on a small patch of the same wooden deck as Image 1, no other stalls, no characters.
- A round base one and a half times as wide as Piko is tall (Piko: the small clear blue jelly with two dark blue horns in Image 2), a little wider than Lumo the fox is tall.
- One steep cone roof that sweeps almost down to the deck: the lower edge of the roof is only half as high as Piko, all the way around. The tip of the cone is twice Piko's height.
- The roof is thick, tightly stretched waxed canvas, smooth and glossy like a slide, in wide vertical stripes of warm terracotta red and cream that match the awnings of Image 1. It looks stiff and slippery, not soft or bouncy. No ropes, no ladders, no flags, no lanterns, no handholds on the roof.
- On the very tip: one round wooden knob like a ball, the size of Lumo's fist.
- Under the low roof edge only a narrow wooden counter rim shows. No goods hanging outside.
- No text, no letters, no signs. Square 1:1, centered with some margin. Plain flat light-gray background around the deck patch, soft even lighting.
```

### Tập 01

Làm trước khi có quy tắc trên, nên đạo cụ có đủ ảnh nhiều góc nhìn để dựng model mà chưa có `_ref` (Seedance dùng ảnh nào: `04_PRODUCTION/SEEDANCE.md`, mục "Ảnh tham chiếu"). Danh sách asset: beat sheet `03_CONTENT/Scripts/EP001_great_rain_experiment.md`.

| Asset | Thư mục | Ảnh | Có |
|---|---|---|---|
| Rain-O-Matic 3000 | `Props/Rain_O_Matic/` | `rain_o_matic_front.png`, `rain_o_matic_back.png`, `rain_o_matic_frost.png` | ✅ |
| Nắp che nút đỏ | `Props/Rain_O_Matic/` | `button_cover_front.png`, `button_cover_side.png` | ✅ |
| Bánh răng vàng | `Props/Golden_Gear/` | `golden_gear_front.png`, `golden_gear_side.png`, `golden_gear_frost.png` | ✅ |
| Móc ròng rọc | `Props/Pulley_Hook/` | `pulley_hook_front.png`, `pulley_hook_side.png` | ✅ |
| Vịt cao su | `Props/Rubber_Duck/` | `rubber_duck_side.png`, `rubber_duck_front.png`, `rubber_duck_gear.png` | ✅ |
| Thìa | `Props/Spoon/` | `spoon_top.png`, `spoon_side.png`, `spoon_bent.png` | ✅ |
| Ô | `Props/Umbrella/` | `umbrella_side.png`, `umbrella_closed.png`, `umbrella_inverted.png` | ✅ |
| Hộp ốc | `Props/Screw_Box/` | `screw_box_front.png`, `screw_box_open.png` | ✅ |
| Cuộn dây của Noah | `Props/Noah_Rope/` | `noah_rope_ref.png` | ✅ |
| Con thuyền | `Environments/Noah_Story/` | `noah_ark_side.png`, `noah_ark_front.png` | ✅ |
| Cầu ván | `Environments/Noah_Story/` | `plank_bridge_side.png`, `plank_bridge_top.png` | ✅ |
| Đôi voi con | `Characters/Baby_Elephants/` | `baby_elephants_ref.png` (thiết kế cả đôi), `baby_elephant_front.png`, `baby_elephant_side.png`, `baby_elephant_back.png` | ✅ |
| Noah | `Characters/Noah/` | `noah_front.png`, `noah_side.png`, `noah_hand_front.png`, `noah_hand_back.png` | ✅ |
| Thú trên boong (thỏ, chim, hươu cao cổ) | `Characters/Ark_Animals/` | `ark_animals_ref.png` (thiết kế cả nhóm) | ✅ |

Không sinh ảnh riêng: mây bé (hiệu ứng dựng trong Blender), chiếc lá khô (theo `Environments/Cloud_Valley/concept/cloud_valley_dry_hero.png`). Bối cảnh thế giới truyện của Noah: chưa có prompt, chưa sinh. Wonder Hub dùng `wonder_hub_island_hero.png` (mục "Tập 000A").

#### Nhân vật phụ

**Đôi voi con** (có diễn: nắm dây và vạt áo choàng bằng vòi, bắt chước nhịp bước của Lumo). Đính kèm `cloud_explorers_character_sheet.png`, lưu `baby_elephants_ref.png`, rồi `baby_elephant_front.png`, `baby_elephant_side.png`, `baby_elephant_back.png`. Voi thứ hai dựng từ model voi thứ nhất, đổi cỡ, tai, chỏm lông theo ảnh thiết kế.
```
The attached sheet shows the four main characters of a soft stylized 3D animated film for young children; use it for style and scale only. Design TWO baby elephants, side characters from a storybook world who want to climb into a big wooden boat to play with their animal friends.
- Cute and round: big heads, short legs, walking on four legs, short trunks that can hold a rope, big soft ears, tiny tails.
- Each about as tall as Lumo the fox; the second one a little smaller.
- Soft warm stone-gray skin with pale pink inner ears. The first one has a small tuft of hair on top of the head; the second one has rounder ears and rosy cheeks, so the two are easy to tell apart. No orange, green, lavender or aqua.
- Shy, sweet expressions, mouths closed with small smiles.
A design sheet: the two elephants side by side in a three-quarter view, standing on four legs. Plain flat light-gray background, soft even lighting. No text, no labels, no logos, no watermark.
```
```
Now only the first (bigger) elephant, as one separate image, in a neutral reference pose: standing on all four legs, legs straight and slightly apart, feet flat, trunk hanging straight down and relaxed, ears relaxed, mouth closed with a small smile, no rope. Seen straight from the front, orthographic, no perspective, centered with some margin, square 1:1. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
```
Now the same elephant in the same neutral pose seen straight from its left side, facing the viewer's left, orthographic, no perspective, same scale, as one separate image: head in a true side profile like the body, trunk hanging straight down, tiny tail hanging down, no rope. The ears stand out sideways as in the front view, so the left ear is seen from behind and edge-on: its gray outer back, foreshortened, with only a thin pink rim, not the pink inner side. Square 1:1, centered with some margin. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
```
Now the same elephant in the same pose seen straight from behind, orthographic, same size and position in the frame as the front view, square 1:1, as one separate image: the gray backs of the two ears standing out sideways exactly as in the front view, the tuft of hair on top of the head, the back, the four legs and the tiny tail hanging down. No rope. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

**Noah** (trong phim chỉ thấy dáng ngược sáng trong nắng vàng ấm trên boong và bàn tay, không thấy rõ mặt: kịch bản tập 01, Cảnh 5). Đính kèm `cloud_explorers_character_sheet.png`, lưu `noah_front.png`, `noah_side.png`, `noah_hand_front.png`, `noah_hand_back.png`.
```
The attached sheet shows the style of a soft stylized 3D animated film for young children; use it for style only. Design kind old Noah from a storybook world, as a shape reference for a character who is only ever seen as a warm backlit silhouette on his boat. ONE image, full body, standing upright and calm, arms relaxed and slightly away from the body, seen straight from the front, orthographic, no perspective.
- Tall and gentle, about two and a half times Lumo's height, broad shoulders, a long simple robe with a rope belt, a hooded cloak, a long soft white beard and long white hair.
- The face is very simple and calm, mostly hidden by the beard and the soft shadow of the hood, with no detailed features.
- Soft rounded stylized shapes, warm earthy colors (sand, brown, cream). No symbols, no text.
- Portrait 2:3, centered with some margin. Plain flat light-gray background, soft even lighting, no ground shadow.
```
```
Now the same figure in the same calm standing pose seen straight from his left side, facing the viewer's left, orthographic, same scale, as one separate image: the outline of the hood, beard, cloak and robe is clear, arms relaxed down at his sides, same sandals. Portrait 2:3. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
```
Now only Noah's right hand and forearm in its cream sleeve, isolated, as one separate image, seen from the palm side with the fingers pointing up: a large, kind, weathered hand in the same style and skin tone, fingers relaxed and slightly open, thumb clearly visible. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
```
Now the very same hand and sleeve turned around, seen from the back of the hand, as one separate image: knuckles and fingernails face the viewer, fingers pointing up in the same spread, so the thumb is now on the opposite side of the image. Same size and position. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

**Thú trên boong** (nhân vật nền Cảnh 5: vẫy gọi đôi voi, reo khi đôi voi lên tới boong). Đính kèm `cloud_explorers_character_sheet.png`, lưu `ark_animals_ref.png`. Chỉ dựng phần thấy trên mạn thuyền.
```
The attached sheet shows the four main characters of a soft stylized 3D animated film for young children; use it for style and scale only. Design the background animals that wave from the deck of Noah's big wooden boat in a storybook world: one rabbit, two small birds and one giraffe whose long neck pops up above the railing.
- Cute, round and simple, so they never compete with the main characters.
- Soft pastel colors that are not orange, green, lavender or aqua; happy expressions with closed-mouth smiles.
A design sheet: each animal in a three-quarter view, waving. Plain flat light-gray background, soft even lighting. No text, no labels, no logos, no watermark.
```

#### Đạo cụ

- Mỗi món một chat, lưu ảnh vào `concept/` của thư mục ghi ở bảng "Tập 01".
- Làm máy Rain-O-Matic trước, vì nắp che nút và móc ròng rọc đính kèm ảnh máy. Làm bánh răng trước con vịt, vì ảnh vịt ngậm bánh răng đính kèm ảnh bánh răng.
- `cloud_explorers_character_sheet.png` (trong `01_BRAND/Character_Bible/`) chỉ để lấy phong cách và cỡ so với nhân vật. Cỡ: "Bảng cỡ", mục "Cỡ tập 01".

**Rain-O-Matic 3000.** Đính kèm `cloud_explorers_character_sheet.png`, lưu lần lượt `rain_o_matic_front.png`, `rain_o_matic_back.png`, `rain_o_matic_frost.png`. Ảnh hiện tại sửa từ ảnh cũ (giữ thiết kế, chỉ dời nút xuống thấp và thu nhỏ ổ bánh răng); sinh mới thì gửi prompt dưới đây. Mặt trước theo bố cục previz Cảnh 2 (`03_CONTENT/Previz_2D/EP001_Great_Rain_Experiment/scene02/build_shot.py`). Bánh răng, móc, dây ròng rọc làm riêng.
```
The attached sheet shows the characters of a soft stylized 3D animated film for young children; use it for style and scale only. Design the Rain-O-Matic 3000, a cute cartoon rain-making machine built by Tavi the inventor. ONE image, seen straight from the front, orthographic, no perspective, no characters.
- Chunky rounded body of riveted pastel metal panels on four short stubby legs; the body is a little taller than Lumo the fox.
- On top of the body: a round glass dome about half as wide as the body, with a small hatch door that is only a thin metal frame; inside the dome, a glowing blue crystal core with one small empty gear socket, about one seventh of the dome width (a coin-sized gear that fits in Tavi's palm). A short chimney nozzle on the top right of the body (no clouds in this image).
- A wooden tripod stands on top of the body over the dome, with a small pulley wheel at its peak (no rope, no hook). The peak is about 1.65 times the height of the body top (almost twice Lumo's height).
- Front face, left half: a round gauge with tick marks and a needle at the top, a round knob below it, and a small pull lever near the bottom. Right half: one big round shiny red push button, about one fifth of the body width, placed LOW: its center at about one third of the height from the ground to the top of the body (legs included), at Lumo's chest height, level with the pull lever and below the copper pipe. A horizontal copper pipe across the upper middle and a small cloud-shaped plate in the lower center.
- It runs on the crystal core: no electric wires, no plugs, no sparks.
- No text, no letters, no numbers anywhere. Playful, handmade, whimsical.
- Centered with some margin, square 1:1. Plain flat light-gray background, soft even lighting, no ground shadow.
```
```
Now the BACK view of the same machine as one separate image: seen straight from behind, orthographic, same size and position in the frame. Exactly the same colors and materials as the front (teal and cream riveted panels, gold rivets and trim, wooden tripod at the same height), no purple or lavender anywhere. The four legs, the glass dome with the crystal core and its small coin-sized gear socket, the tripod with its pulley and the chimney nozzle seen from behind (the nozzle is now on the left); no gauge, knob, lever, button or cloud plate on this side. No text. Plain flat light-gray background, soft even lighting, no ground shadow.
```
```
Now the same machine from the same front view, as one separate image, same size and position in the frame, same teal and cream colors, button still low on the right, in its overcooled state:
- The glass dome is covered with thick white frost and puffs of cold mist; through the frost, a small golden gear sitting in the small socket glows bright gold.
- The small hatch door is frozen and has popped slightly open.
- The pulley rope hangs from the pulley, frozen stiff and white with ice.
- The gauge needle is pushed past the last tick mark and frozen, with frost on the gauge glass; the knob is turned all the way.
- Small icicles along the edge of the dome and the top of the body; the rest of the machine is wet with cold dew.
- Still cute and funny, never scary. No text. Plain flat light-gray background, soft even lighting, no ground shadow.
```

**Nắp che nút đỏ** (Cảnh 7). Đính kèm `rain_o_matic_front.png`, lưu `button_cover_front.png` (lắp trên máy), rồi `button_cover_side.png` (riêng cái nắp).
```
The attached image is the Rain-O-Matic 3000 from a soft stylized 3D animated film for young children. Tavi the inventor has built an over-the-top safety cover for its big red button. Create ONE image of the same machine, same front view, same size and position in the frame, with the cover fitted over the red button:
- A clear dome-shaped cover, about three times as wide as the button, so the red button still shows through it. The button stays exactly where it is, low on the right of the front.
- A sturdy hinged frame with the hinge on the dome's LEFT edge, a chunky coiled spring standing upright on its RIGHT edge, a big latch with a lock at its BOTTOM FRONT, and a small round warning light on top, lit warm orange. Nothing under the cover: no spring below it.
- Same pastel riveted metal and brass as the machine; handmade and a little silly.
- No text, no letters, no numbers. Plain flat light-gray background, soft even lighting, no ground shadow.
```
```
Now only the cover, removed from the machine and isolated, as one separate image, orthographic, no perspective. Keep the parts where they are on the machine: hinge on the dome's left edge, coiled spring on its right edge, lock at the bottom front, warning light on top. Show the cover seen exactly from the spring side (as if walking to the right of the front view and looking at it from there): the front of the cover, with the latch and lock sticking out, faces the viewer's left; the coiled spring faces the viewer, in the middle; the hinge is on the far side and hidden; the dome shows its full depth. Same design, colors and scale. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

**Bánh răng vàng** (rơi ra từ Chronicle Engine trong Wonder Hub, đài thiên văn cổ: `03_CONTENT/README.md`). Đính kèm `cloud_explorers_character_sheet.png`, lưu `golden_gear_front.png`, `golden_gear_side.png`, `golden_gear_frost.png`.
```
The attached sheet shows the style of a soft stylized 3D animated film for young children; use it for style only. Design a mysterious golden gear that came from an ancient machine inside an old observatory. ONE image, the gear seen straight from the front, orthographic, no perspective, isolated.
- Warm polished gold, eight chunky rounded teeth, a lighter gold inner disc and a softly glowing pale-gold center hub.
- A faint engraved pattern of tiny stars and orbits on the inner disc, like an old astronomer's instrument.
- Small: it fits in a rubber duck's beak and in the palm of Tavi's hand.
- No text, no letters, no numbers. Plain flat light-gray background, soft even lighting, no ground shadow.
```
```
Now the same gear seen edge-on from the side, orthographic, same scale, as one separate image: the thickness of the gear, the teeth and the center hub are clear. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
```
Now the same gear from the same front view, as one separate image, covered with white frost and tiny ice crystals; the gold still glows faintly through the frost and a few small ice beads bounce off it. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

**Móc ròng rọc.** Đính kèm `rain_o_matic_front.png`, lưu `pulley_hook_front.png`, `pulley_hook_side.png`. Móc phải nhỏ đủ để thả lọt qua cửa nhỏ trên vòm kính (Cảnh 6).
```
The attached image is the Rain-O-Matic 3000 with its pulley tripod, from a soft stylized 3D animated film for young children. Design its pulley hook as ONE separate object: a chunky cartoon metal hook in dark gray with a rounded blunt tip, an eye ring at the top with a short piece of pale rope tied to it. About the size of Lumo the fox's paw, small enough to drop through a small hatch in the glass dome. Seen straight from the front, orthographic, no perspective, isolated, only the hook (no machine). Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
```
Now the same hook seen straight from the side, rotated 90 degrees, orthographic, same scale, as one separate image: the thickness of the hook, the eye ring seen edge-on and the rope knot are clear. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

**Vịt cao su.** Đính kèm `cloud_explorers_character_sheet.png`, lưu `rubber_duck_side.png`, `rubber_duck_front.png`. Ảnh thứ ba đính kèm thêm `Props/Golden_Gear/concept/golden_gear_front.png`, lưu `rubber_duck_gear.png`.
```
The attached sheet shows the style of a soft stylized 3D animated film for young children; use it for style only. Design a classic rubber duck toy that Piko the jelly creature pulls out of a magic pouch and keeps as a favorite. ONE image, the duck seen straight from the side facing right, orthographic, no perspective, isolated.
- Bright yellow soft rubber, an orange beak with a small gap between its upper and lower halves (it can hold a small gear), small dark dot eyes, a little upturned tail, a round chubby body with a flat bottom so it floats upright.
- Small: about one sixth of Piko's height, so Piko can hug it with both stubby arms.
- No text, no logos. Plain flat light-gray background, soft even lighting, no ground shadow.
```
```
Now the same duck seen straight from the front, orthographic, same scale, as one separate image. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
```
Now the same duck in a three-quarter view as one separate image, holding the attached golden gear in its beak by the edge of the gear, upright between the upper and lower halves of the beak; the gear glints. Same duck design, colors and proportions. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

**Thìa** (Cảnh 1). Đính kèm `cloud_explorers_character_sheet.png`, lưu `spoon_top.png`, `spoon_side.png`, `spoon_bent.png`.
```
The attached sheet shows the style of a soft stylized 3D animated film for young children; use it for style only. Design an ordinary but cute metal spoon that Piko the jelly creature pulls out of a magic pouch. ONE image, the spoon seen straight from above, orthographic, no perspective, isolated, bowl at the top and handle pointing down.
- Polished silver-gray metal with soft rounded edges, an oval bowl, a slightly chunky handle with a rounded end. No engraving.
- About a quarter of Piko's height.
- No text, no logos. Plain flat light-gray background, soft even lighting, no ground shadow.
```
```
Now the same spoon seen straight from the side, orthographic, same scale, as one separate image: the curve of the bowl and the thickness of the handle are clear. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
```
Now the same spoon after digging very hard ground, side view, same scale, as one separate image: the handle is bent into a U shape in the middle, and the bowl has a little dry dirt on it. Funny, not broken. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

**Ô** (Cảnh 7). Đính kèm `cloud_explorers_character_sheet.png`, lưu `umbrella_side.png`, `umbrella_closed.png`, `umbrella_inverted.png`.
```
The attached sheet shows the style of a soft stylized 3D animated film for young children; use it for style only. Design a small umbrella that Piko the jelly creature pulls out of a magic pouch. ONE image: the umbrella open, seen straight from the side, orthographic, no perspective, isolated.
- A round canopy of eight panels in soft pastel pink with small white polka dots, rounded tips, a short wooden shaft and a curved wooden handle.
- Sized for Piko: the open canopy is a little wider than Piko's body.
- No text, no logos. Plain flat light-gray background, soft even lighting, no ground shadow.
```
```
Now the same umbrella closed and folded, seen straight from the side, same scale, as one separate image. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
```
Now the same umbrella blown inside out by the wind, as one separate image, same scale: the canopy flipped upward like a bowl and full of clear rain water to the brim, the handle pointing down, seen from the side and slightly above so the water surface shows. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

**Hộp ốc** (Nori xếp ốc theo cỡ ở Cảnh 2; cuối Cảnh 6 bánh răng được cất vào đây, Tavi đóng nắp). Đính kèm `cloud_explorers_character_sheet.png`, lưu `screw_box_front.png`, `screw_box_open.png`.
```
The attached sheet shows the style of a soft stylized 3D animated film for young children; use it for style only. Design the screw box of Tavi the inventor: a small wooden box with a hinged lid. ONE image: the box closed, seen straight from the front, orthographic, no perspective, isolated.
- Warm honey-brown wood with rounded edges, brass corner caps, a brass hinge at the back and a simple brass latch at the front.
- About half as wide as Tavi is tall.
- No text, no letters, no numbers. Plain flat light-gray background, soft even lighting, no ground shadow.
```
```
Now the same box with the lid open, seen from the front and a little above, as one separate image: inside, three compartments from left to right hold big, medium and small chunky cartoon screws with round heads, neatly sorted by size. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

**Cuộn dây của Noah** (Cảnh 5–6: dắt đôi voi, rồi buộc móc ròng rọc vào đầu dây để rút bánh răng; độ dài dây chỉnh trong Blender). Đính kèm `cloud_explorers_character_sheet.png`, lưu `noah_rope_ref.png`.
```
The attached sheet shows the style of a soft stylized 3D animated film for young children; use it for style only. Design a small coil of thick natural rope that kind old Noah drops from his big wooden boat. ONE image, seen straight from the front, orthographic, isolated: a neat round coil of golden-tan twisted hemp rope, with one loose end hanging down. Small enough for Lumo the fox to hold in front of the belly with both paws. No text. Plain flat light-gray background, soft even lighting, no ground shadow.
```

**Con thuyền.** Đính kèm `01_BRAND/Brand_Guideline/world_key_art.png`, lưu `noah_ark_side.png`, `noah_ark_front.png`. Thú trên boong không nằm trong ảnh này.
```
The attached image is a style reference only (soft stylized 3D animated film for young children). Design Noah's giant wooden boat for a storybook world. ONE image: the whole boat seen straight from the side, orthographic, no perspective, isolated, floating level; no water, no characters, no animals.
- A huge, gentle, rounded wooden ark, as tall as a small hill: a long chunky hull of warm honey-brown planks with soft rounded edges, a simple wooden house with a pitched roof on the deck, small round windows along the house, a wooden railing around the deck with one opening for a plank ramp. No ramp in this image (the ramp is a separate object); below the opening, show the hull planks.
- Handmade and cozy, never scary. No flags, no symbols, no text.
- Wide 16:9. Plain flat light-gray background, soft even lighting, no ground shadow.
```
```
Now the same boat (without a ramp) seen straight from the front (the bow), orthographic, same scale, as one separate image. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

**Cầu ván** (bắc từ mỏm đồi lên mạn thuyền; Nori để một chấm sáng trên từng nẹp, Lumo bước lên từng chấm). Đính kèm `world_key_art.png`, lưu `plank_bridge_side.png`, `plank_bridge_top.png`.
```
The attached image is a style reference only (soft stylized 3D animated film for young children). Design a long wooden plank ramp for walking animals up into a big wooden boat. ONE image, the ramp lying flat and seen straight from the side, orthographic, no perspective, isolated (it is tilted into place later in 3D).
- Two or three wide weathered planks side by side, eight evenly spaced wooden cleats nailed across the top, rope lashings at both ends, soft rounded edges, warm wood.
- Wide enough for a baby elephant to walk on.
- No text. Wide 16:9. Plain flat light-gray background, soft even lighting, no ground shadow.
```
```
Now the same ramp seen straight from above, orthographic, same scale, as one separate image, with the eight cleats clearly visible. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

## Bộ ảnh dựng model

Chỉ làm cho asset sắp dựng model trong Blender. Mỗi ảnh một góc nhìn, nền trơn. Ảnh nhìn sau đi cặp với ảnh nhìn trước cùng tên, thêm hậu tố `_back`. Mỗi nhân vật có:

- **Thân** (`<tên>_apose_body.png`, `<tên>_tpose_body.png`): chỉ phần dựng liền vào thân. Bỏ đồ rời và phần làm riêng (áo choàng, túi, ba lô, đuôi, cánh, râu, lá đội đầu); đồ ôm sát (mũ, kính, gile của Tavi) để liền. Dùng để dựng lưới thân và đặt xương.
- **Đủ đồ** (`<tên>_outfit.png`): ảnh thân A-pose mặc đủ đồ, giữ nguyên tư thế, cỡ và vị trí trong khung để chồng khớp lên ảnh thân. Dùng để dựng và đặt đồ rời. Không cần bản T-pose vì đồ rời dựng trên tư thế A.
- **Bộ phận làm riêng** (`<tên>_<bộ phận>_ref.png`): đuôi, cánh, áo choàng, túi.

Đạo cụ: ảnh nhìn thẳng trước, sau (`<tên>_front.png`, `<tên>_back.png`). Ảnh `<tên>_ref.png` nhìn 3/4 có sẵn chỉ để tham khảo thiết kế.

Ngoại lệ:
- Vật có hai mặt như nhau (bánh răng, thìa, móc) hoặc vật dài (thuyền, cầu ván): thay ảnh sau bằng ảnh nhìn ngang (`_side`) hoặc nhìn từ trên (`_top`).
- Thú bốn chân: ảnh trước, ngang, sau; không có A-pose, T-pose.
- Đạo cụ đổi hình trong phim có thêm ảnh trạng thái (`_frost`, `_bent`…).

### Hiện trạng

Ảnh nằm trong `concept/` của asset. ✅ có, ❌ chưa có. Ảnh thân cố ý không có đuôi và đồ rời; đuôi chỉ có ở ảnh đủ đồ và ảnh `_tail_ref`.

| Nhân vật | Thân A-pose (trước · sau) | Thân T-pose (trước · sau) | Đủ đồ (trước · sau) | Làm riêng |
|---|---|---|---|---|
| Lumo | ✅ · ✅ | ✅ · ✅ | ✅ · ✅ | áo choàng ✅ `lumo_cape_ref.png`, túi ✅ `lumo_bag_ref.png`, đuôi ✅ `lumo_tail_ref.png` |
| Tavi | ✅ · ✅ | ✅ · ✅ | ✅ · ✅ | đuôi ✅ `tavi_tail_ref.png` |
| Nori | ✅ · ✅ | ✅ · ✅ | ✅ · ✅ | cánh ✅ `nori_wing_ref.png` |
| Piko | ✅ · ✅ | ✅ · ✅ | ✅ · ✅ `piko_pouch_ref.png` (nhìn 3/4), `piko_pouch_ref_back.png` | — |
| Sinh vật nhỏ (`Valley_Critters/`, tên file `valley_critter_…`) | ✅ · ✅ | ✅ · ✅ | — | lá đội đầu: theo `valley_critters_ref.png` ✅ |

| Đạo cụ | Trước · sau |
|---|---|
| Wonder Compass (Lumo) | ✅ · ✅ |
| Inventor Pack (Tavi) | ✅ · ✅ |
| Story Lens (Nori) | ✅ · ✅ |
| Pocket of Wonders (Piko) | ✅ · ✅ |

Bốn nhân vật chính có ảnh xoay `<tên>_turnaround.png` ghép từ ảnh đủ đồ (Piko: `piko_pouch_ref.png` và `piko_pouch_ref_back.png`); ảnh đủ đồ đổi thì ghép lại.

Ảnh lệch nhau, khi dựng theo:
- **Đuôi Tavi:** số và cỡ tinh thể theo ảnh đủ đồ (`tavi_outfit.png`, `tavi_outfit_back.png`: 5–6 tinh thể nhỏ); `tavi_tail_ref.png` (4 tinh thể to) chỉ lấy dáng đuôi và màu.
- **Inventor Pack:** cỡ và chi tiết theo `inventor_pack_front.png`, `inventor_pack_back.png`; ảnh đủ đồ của Tavi chỉ để đặt chỗ (nhìn trước ba lô lộ rộng ra hai vai hơn nhìn sau). Cờ lê, dụng cụ ở túi bên chỉ có trong ảnh trước: dựng theo ảnh trước, nhìn sau vẫn thấy phần nhô lên.
- **Story Lens:** hai viên đá tím ở hai bên vành chỉ có trong ảnh trước: dựng theo ảnh trước; đá gắn trên vành nên nhìn sau thấy gờ của nó.

### Chuẩn ảnh dựng model

Trong Blender, ảnh trước đặt làm ảnh nền (Reference) ở Front view, ảnh sau ở Back view, scale theo chiều cao trong Character Bible. Ảnh sai tư thế hoặc hai ảnh lệch cỡ thì model sai theo, nên soát từng ảnh trước khi dùng:

1. **Tư thế đối xứng, tay thẳng.** A-pose: tay dang chéo xuống khoảng 45°. T-pose: tay dang ngang tầm vai, song song mặt đất. Khe hở rõ giữa tay và thân. Nhân vật có chân: chân thẳng, bàn chân đặt phẳng, rộng bằng vai, mũi chân hướng ra trước, có khe hở giữa hai chân.
   - A-pose: vai biến dạng đẹp hơn khi tay buông xuống (tư thế hay gặp nhất). T-pose: tay xa thân nhất, dễ thấy vai, khuỷu, cổ tay; hợp với nhân vật bụng tròn tay ngắn như Lumo, Tavi.
   - Dựng lưới theo tư thế nào: thử với Lumo, tư thế nào qua bước kiểm tra rig (mục "Dựng trong Blender") tốt hơn thì dùng cho cả nhóm.
2. **Bàn tay úp:** lòng bàn tay hướng xuống đất, ngón duỗi thẳng và hơi tách nhau, ngón cái hướng ra trước. Dựng theo tay ngửa thì cổ tay ở tư thế nghỉ đã xoắn, animation trông gượng.
3. **Thấy rõ khớp** để đặt xương: cằm và cổ, vai, khuỷu, cổ tay, háng, đầu gối, cổ chân.
4. **Biểu cảm trung tính:** miệng khép, cười nhẹ, mắt mở nhìn thẳng. Biểu cảm do face rig làm.
5. **Máy quay:** chính diện, trực giao (không phối cảnh), ngang tầm ngực; thấy trọn từ chóp tai, sừng, râu tới bàn chân, chừa lề. Nhân vật khổ dọc 2:3, đạo cụ khổ vuông (Story Lens khổ dọc).
6. **Cặp trước, sau khớp nhau:** cùng cỡ, cùng vị trí trong khung. Lật ngang ảnh sau rồi chồng mờ 50% lên ảnh trước: viền ngoài phải gần trùng. ChatGPT có thể trả khổ khác ảnh gửi kèm (1122×1402 so với 1086×1448), nên so theo chiều cao nhân vật, không theo khung ảnh. Trong ảnh sau, bên phải của nhân vật nằm bên phải người xem.
7. **Nền, ánh sáng:** nền xám nhạt trơn, ánh sáng đều, không bóng đổ xuống đất, không chữ, chỉ một đối tượng.
8. **Trong suốt, phát sáng làm bằng shader** (thân thạch của Piko, ánh sáng của Nori, tinh thể của Tavi), ảnh chỉ cần rõ hình. Ảnh thân bỏ bọt trong thân và giọt nước quanh Piko, bỏ quầng sáng quanh Nori để thấy rõ viền.

### Prompt dựng model

Cách gửi, tải, sửa: "Sinh ảnh bằng ChatGPT". Ảnh T-pose sửa từ ảnh A-pose đã duyệt, ảnh sau sửa từ ảnh trước (cùng mục đó).

#### Lumo: ảnh sau của thân

Đính kèm `Characters/Lumo/concept/lumo_apose_body.png`, lưu `lumo_apose_body_back.png`:
```
The attached image is the approved FRONT view of Lumo, a cute chibi fox character from a soft stylized 3D animated film for young children. Create the BACK view of exactly the same character as one separate image.
- Seen from directly behind, orthographic, no perspective distortion, camera at chest height.
- Exactly the same A-pose (arms straight, about 45 degrees down, palms facing down), same proportions and head size, same size and position in the frame, same canvas: the ear tips and the feet at the same height as in the front image.
- Seen from behind, Lumo's right arm is on the viewer's right.
- The very large ears keep exactly the same shape, size and outward spread as in the front view. Their backs are orange fur all the way to the tips, the same orange as the front of the ears (no cream or white tip); the pink is only on the inside. The cream tuft stays on top of the head; the back of the head, the neck, the back and the backs of the arms and legs are orange fur. Cream paws and cream feet.
- NO tail: the lower back and bottom are smooth orange fur. No cape, no bag, no clothes.
- Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
Đính kèm theo thứ tự `lumo_apose_body_back.png`, `lumo_tpose_body.png`; lưu `lumo_tpose_body_back.png`:
```
Image 1 is the approved A-pose BACK view, Image 2 the approved T-pose FRONT view. Create the T-pose BACK view as one separate image: use Image 1 as the base and edit ONLY the arms, rotating each whole arm at the shoulder up to point straight out horizontally, parallel to the ground, exactly like the arms in Image 2 (seen from behind). Everything else stays identical to Image 1: head, ears, body, size and position in the frame. The arms keep the same thickness and length.
```

#### Lumo: đủ đồ

Đính kèm theo thứ tự `lumo_apose_body.png`, `lumo_cape_ref.png`, `lumo_bag_ref.png`; lưu `lumo_outfit.png`:
```
Image 1 is Lumo's approved front view (body only), from a soft stylized 3D animated film for young children. Image 2 is Lumo's red cape, Image 3 is Lumo's brown shoulder bag. Create ONE new image: Image 1 exactly as it is (same pose, proportions, face, size and position in the frame, same canvas), now wearing the cape and the bag, with the tail.
- Cape from Image 2: red, round gold clasp at the front of the neck, gold cloud pattern along the lower edge. It is LONG: it reaches the knees. It hangs behind the arms; the arms, chest and belly stay visible.
- Bag from Image 3 with its gold cloud buckle, resting on the front of the belly on Lumo's right side (the viewer's left). The strap runs diagonally from the bag up over Lumo's LEFT shoulder (the viewer's right).
- Tail: a big fluffy fox tail, orange with a cream-white tip. It comes out of the lower back through a vertical slit in the middle of the back of the cape and curves out to Lumo's left side (the viewer's right), so part of it shows next to the leg.
- Mouth closed with a gentle smile, eyes looking straight at the camera, as in Image 1.
- Orthographic front view, no perspective distortion. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
Lưu `lumo_outfit_back.png`:
```
Now create the BACK view of this outfit image as one separate image: seen from directly behind, orthographic, same pose, same size and position in the frame, same canvas. Seen from behind, Lumo's right side is on the viewer's right.
- The red cape covers the back from the neck down to the knees, with the gold cloud pattern along its lower edge as in Image 2, and no other emblem.
- The bag strap crosses the back diagonally from Lumo's left shoulder (the viewer's left) down to the right hip (the viewer's right), where only the edge of the bag shows.
- The fluffy tail comes out through a vertical slit in the middle of the back of the cape, at the lower back, with its cream-white tip.
- The backs of the ears are orange fur all the way to the tips, no cream or white tip.
- Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
Lưu `lumo_tail_ref.png`:
```
From this image, show only Lumo's tail as a separate object: side view, isolated, full length from the root to the tip, same fur, colors and size. No character. Plain flat light-gray background, soft even lighting, no text.
```

#### Tavi: thân

Đính kèm `Characters/Tavi/concept/tavi_outfit.png` (ảnh gốc cũ đã xoá; ảnh thân đã sinh xong, bước này chỉ để gen lại), lưu `tavi_apose_body.png`:
```
Edit this image of Tavi, a cute chibi reptile inventor from a soft stylized 3D animated film for young children. Create ONE image in a symmetrical A-pose: arms straight, angled about 45 degrees down from the shoulders. Keep the design, head size, proportions, colors, crystal spikes, leather aviator cap and goggles exactly the same, and apply all of these:
1. Remove the backpack with its blueprint roll and crystal tubes, the belt pouch, the glass tube on the belt and the wrist cuffs. Keep only the fitted beige vest and a simple brown belt.
2. Remove the tail completely. Keep the crystal spikes on the back of the head and along the spine, close to the body.
3. Clear gap between the arms and the body, and between the arms and the crystal spikes.
4. Hands: palms facing down toward the ground (not toward the camera), four fingers straight and slightly apart, thumbs pointing forward.
5. Legs straight, feet flat on the ground, shoulder-width apart, toes pointing forward, clear gap between the legs.
6. Mouth closed with a gentle smile, eyes open looking straight at the camera.
7. Orthographic front view at chest height, no perspective distortion, whole body visible from the top of the spikes to the feet with some margin, centered. Portrait 2:3.
8. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
Đính kèm `tavi_apose_body.png`, lưu `tavi_tpose_body.png`:
```
Use the attached approved A-pose as the base and edit ONLY the arms: rotate each whole arm at the shoulder joint up to a straight T-pose, horizontal at shoulder height, parallel to the ground, palms facing down. Everything else stays identical to the attached image: head, face, cap, goggles, the crystal spikes (including those along both sides of the torso), vest, belt, belly, legs, feet, size and position in the frame. The arms keep exactly the same thickness, length and plain green color: no sleeves, no shoulder pads. One separate image, plain flat light-gray background, no ground shadow, no text.
```
Đính kèm `tavi_apose_body.png`, lưu `tavi_apose_body_back.png`:
```
The attached image is the approved A-pose FRONT view of Tavi. Create its BACK view as one separate image: seen from directly behind, orthographic, exactly the same pose, proportions, size and position in the frame, same canvas. Seen from behind, Tavi's right arm is on the viewer's right.
- The glowing teal crystal crest is wide: a central row of spikes from the top of the head down the spine, plus smaller spikes angled outward on both sides of the back, so that they stick out past both sides of the torso at the same places and sizes as in the front view. Biggest on the head and shoulders, smaller toward the lower back.
- The back of the leather aviator cap and the goggle strap around the back of the head.
- The back of the fitted beige vest and the simple brown belt. No backpack, no pouches.
- NO tail: the lower back and bottom are smooth green skin.
- Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
Đính kèm theo thứ tự `tavi_apose_body_back.png`, `tavi_tpose_body.png`; lưu `tavi_tpose_body_back.png`:
```
Image 1 is the approved A-pose BACK view, Image 2 the approved T-pose FRONT view. Create the T-pose BACK view as one separate image: use Image 1 as the base and edit ONLY the arms, rotating each whole arm at the shoulder up to a straight T-pose exactly like the arms in Image 2 (seen from behind). Everything else stays identical to Image 1: the wide crystal crest with the side spikes, cap, vest, belt, legs, size and position in the frame. Arms the same thickness and plain green. No tail, no backpack.
```

#### Tavi: đủ đồ

Đính kèm theo thứ tự `tavi_apose_body.png`, `Props/Inventor_Pack/concept/inventor_pack_ref.png`; lưu `tavi_outfit.png`:
```
Image 1 is Tavi's approved front view (body only), from a soft stylized 3D animated film for young children. Image 2 is Tavi's backpack, the Inventor Pack. Create ONE new image: Image 1 exactly as it is (same pose, proportions, face, size and position in the frame, same canvas), now with the full outfit and the tail:
- A brown leather belt pouch with a gold cloud emblem on Tavi's right hip (the viewer's left), a small glowing glass tube hanging from the belt on Tavi's left hip (the viewer's right), brown leather wrist cuffs.
- The Inventor Pack from Image 2 worn on the back: two shoulder straps over the front of the shoulders, the blueprint roll on top and the glowing crystal tubes peeking out at the sides.
- Tail: green with a cream underside and small teal crystal spikes along its top, coming out from the lower back and curving out to Tavi's right side (the viewer's left), so part of it shows next to the leg.
- Hands palms down, mouth closed with a gentle smile, as in Image 1.
- Orthographic front view, no perspective distortion. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
Đính kèm theo thứ tự `tavi_outfit.png`, `tavi_apose_body_back.png`, `Props/Inventor_Pack/concept/inventor_pack_ref.png`; lưu `tavi_outfit_back.png`:
```
Image 1 is Tavi's approved outfit FRONT view. Image 2 is Tavi's approved BACK view without the outfit. Image 3 is the Inventor Pack. Create the BACK view of the outfit as one separate image: seen from directly behind, orthographic, same pose as Image 1 and Image 2, same size and position in the frame, same canvas. Seen from behind, Tavi's right side is on the viewer's right. Use Image 2 as the base (same head, cap, goggle strap, crystal crest, arms, legs) and add:
- The Inventor Pack worn on the middle of the back: we see its outer face as in Image 3 (gear emblem, buckles, blueprint roll on top, glowing crystal tubes on both sides). It hangs below the big crystal spikes of the head and shoulders; the spikes do not pass through the pack; the side spikes still peek out past both sides of the torso.
- The brown leather wrist cuffs, the belt with its pouch and glass tube seen from behind.
- The tail comes out from the lower back below the pack, green with a cream underside and small teal crystal spikes along its top, curving to Tavi's right side (the viewer's right).
- Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
Lưu `tavi_tail_ref.png`:
```
From these outfit images, show only Tavi's tail as a separate object: side view, isolated, full length from the root to the tip, green with a cream underside and its small teal crystal spikes along the top, same colors and size. No character. Plain flat light-gray background, soft even lighting, no text.
```

#### Nori: thân

Đính kèm `Characters/Nori/concept/nori_outfit.png` (ảnh gốc cũ đã xoá; ảnh thân đã sinh xong, bước này chỉ để gen lại), lưu `nori_apose_body.png`:
```
Edit this image of Nori, a small glowing light spirit from a soft stylized 3D animated film for young children. Create ONE image. Keep the round lavender body (head and body are one round shape), face, eyes, rosy cheeks and tiny arms exactly the same, and change only the following:
1. Remove all four wings completely.
2. Remove both antennae and their stars completely.
3. Remove the golden light trail under the body; the bottom of the body is smoothly round, no feet.
4. The tiny arms grow smoothly out of the lower sides of the round body (the shoulder blends into the body, no gap and no flat cut), held straight out, angled about 45 degrees down, with a clear gap only between the underside of each arm and the body, palms facing down.
5. Mouth closed with a gentle smile, eyes open looking straight at the camera.
6. Orthographic front view, no perspective distortion, Nori centered with some margin. Portrait 2:3.
7. Plain flat light-gray background, soft even lighting, no glow halo around the body, no ground shadow, no text.
```
Đính kèm `nori_apose_body.png`, lưu `nori_tpose_body.png`:
```
Use the attached approved image as the base and edit ONLY the tiny arms: rotate each arm at the shoulder up to point straight out horizontally, parallel to the ground. The shoulder stays exactly where it is now, low on the side of the round body: the arm pivots there and does not move higher up the body, and the shoulder blends smoothly into the body as in the attached image, no flat seam. Everything else stays identical: body, face, size and position in the frame. The arms keep the same size and shape. One separate image, plain flat light-gray background, no glow halo, no text.
```
Đính kèm `nori_apose_body.png`, lưu `nori_apose_body_back.png`:
```
Create the BACK view of the attached approved front image as one separate image: seen from directly behind, orthographic, same pose, same size and position in the frame, same canvas. Seen from behind, Nori's right arm is on the viewer's right. The back is one smooth round lavender surface: no face, no wings, no antennae, no feet. Plain flat light-gray background, soft even lighting, no glow halo, no ground shadow, no text.
```
Đính kèm theo thứ tự `nori_apose_body_back.png`, `nori_tpose_body.png`; lưu `nori_tpose_body_back.png`:
```
Image 1 is the approved A-pose BACK view, Image 2 the approved T-pose FRONT view. Create the T-pose BACK view as one separate image: use Image 1 as the base and edit ONLY the tiny arms, rotating them up to point straight out horizontally exactly like the arms in Image 2 (seen from behind), from the same low shoulder spot on the side of the round body, at exactly the same height as in Image 2, the shoulder blending smoothly into the body with no flat seam. Everything else stays identical to Image 1.
```

#### Nori: đủ đồ

Đính kèm theo thứ tự `nori_apose_body.png`, `nori_wing_ref.png`; lưu `nori_outfit.png`:
```
Image 1 is Nori's approved front view (body only), from a soft stylized 3D animated film for young children. Image 2 shows Nori's right upper and lower wings. Create ONE new image: Image 1 exactly as it is (same pose, face, size and position in the frame, same canvas; the round body keeps exactly the same diameter and position, do not shrink it to make room for the wings), now with:
- Four transparent wings like those in Image 2, mirrored for the left side (two bigger upper wings, two smaller lower wings), attached to the back of the body and spreading out to both sides.
- Two thin lavender antennae on top of the head, curving outward, each ending in a small glowing pale-yellow star.
- No feet: under the round body, a short soft trail of golden light that fades out, in place of legs.
- A gentle glow, but the body outline stays sharp and easy to read.
- Orthographic front view, no perspective distortion. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
Đính kèm theo thứ tự `nori_outfit.png`, `nori_apose_body_back.png`; lưu `nori_outfit_back.png`:
```
Image 1 is Nori's approved outfit FRONT view. Image 2 is Nori's approved BACK view without wings and antennae. Create the BACK view of the outfit as one separate image: use Image 2 as the base (same round body, arms, size and position in the frame, same canvas) and add the same four transparent wings, the two antennae with glowing stars and the golden light trail as in Image 1, all seen from directly behind. Each wing keeps the same size, angle and position as in Image 1, mirrored left to right: the upper wings do not rise higher and the lower wings do not shrink. Seen from behind, Nori's right side is on the viewer's right. Show clearly where the four wings join the upper back and where the antennae rise from the top of the head. No face. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
Đính kèm `nori_outfit.png`, lưu `nori_wing_ref.png`:
```
From the attached image, show only Nori's two right wings (one upper, one lower) as separate objects, laid out flat and seen straight on, isolated, with their vein pattern and color gradient clearly visible. No character. Plain flat light-gray background, soft even lighting, no text.
```

#### Piko: thân

Đính kèm `Characters/Piko/concept/piko_pouch_ref.png` (ảnh gốc cũ đã xoá; ảnh thân đã sinh xong, bước này chỉ để gen lại), lưu `piko_apose_body.png`:
```
Edit this image of Piko, a jelly creature from a soft stylized 3D animated film for young children. Create ONE image. Keep the body shape, the glossy aqua jelly look, the two dark-blue horns, eyes, cheeks and proportions exactly the same, and change only the following:
0. Remove the pouch and its gold cord completely.
1. Mouth closed with a playful smile, no teeth or tongue visible, eyes open looking straight at the camera.
2. The two stubby arms grow out of the sides of the body like soft rounded jelly buds, joined smoothly at the shoulder with no gap there, angled about 45 degrees below horizontal (an A-pose, not almost horizontal); a clear gap only between the underside of each arm and the body below it. The arms never float apart from the body.
3. No bubbles inside the body and no water drops around it.
4. No legs: the wide rounded bottom rests on the ground.
5. Orthographic front view, no perspective distortion, Piko centered with some margin, from the horn tips to the bottom. Portrait 2:3.
6. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
Đính kèm `piko_apose_body.png`, lưu `piko_tpose_body.png`:
```
Use the attached approved image as the base and edit ONLY the stubby arms: rotate each arm at the shoulder up to point straight out horizontally, parallel to the ground. Each arm stays joined to the body at the same shoulder spot, no gap at the shoulder. Everything else stays identical: body, horns, face, size and position in the frame. The arms keep the same size and shape. One separate image, plain flat light-gray background, no text.
```
Đính kèm `piko_apose_body.png`, lưu `piko_apose_body_back.png`:
```
Create the BACK view of the attached approved front image as one separate image: seen from directly behind, orthographic, same pose, same size and position in the frame, same canvas. Seen from behind, Piko's right arm is on the viewer's right. The two dark-blue horns seen from behind; the back is one smooth glossy aqua jelly surface with no face, no bubbles, no pouch, no cord. The arms stay joined to the body at the shoulder exactly as in the front image. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
Đính kèm theo thứ tự `piko_apose_body_back.png`, `piko_tpose_body.png`; lưu `piko_tpose_body_back.png`:
```
Image 1 is the approved A-pose BACK view, Image 2 the approved T-pose FRONT view. Create the T-pose BACK view as one separate image: use Image 1 as the base and edit ONLY the stubby arms, rotating them up to point straight out horizontally exactly like the arms in Image 2 (seen from behind), at exactly the same height on the body as in Image 2, still joined to the body at the shoulder. Everything else stays identical to Image 1.
```

#### Sinh vật nhỏ của thung lũng: thân

Đính kèm `Characters/Valley_Critters/concept/valley_critters_ref.png`, lưu `valley_critter_apose_body.png`:
```
The attached sheet shows the tiny creatures of the Valley of Clouds, background characters of a soft stylized 3D animated film for young children. Create ONE image of one creature with exactly the same design (pale peach-beige bean-shaped body, lighter belly, dot eyes, rosy cheeks, tiny stubby arms and feet) in a neutral reference pose:
1. Standing upright, symmetrical, arms straight out from the body angled about 45 degrees down, clear gap between the arms and the body; feet flat on the ground, slightly apart, clear gap between them.
2. No leaf on the head: the top of the head is visible.
3. Mouth closed with a small smile, eyes looking straight at the camera.
4. Orthographic front view, no perspective distortion, centered with some margin. Portrait 2:3.
5. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
Đính kèm `valley_critter_apose_body.png`, lưu `valley_critter_tpose_body.png`:
```
Use the attached approved image as the base and edit ONLY the arms: rotate each arm at the shoulder up to point straight out horizontally, parallel to the ground. Everything else stays identical: body, face, feet, size and position in the frame. The arms keep the same size and shape. One separate image, plain flat light-gray background, no text.
```
Đính kèm `valley_critter_apose_body.png`, lưu `valley_critter_apose_body_back.png`:
```
Create the BACK view of the attached approved front image as one separate image: seen from directly behind, orthographic, same pose, same size and position in the frame, same canvas. Seen from behind, the creature's right arm is on the viewer's right. A smooth peach-beige back, no face, no leaf, no tail, no wings. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
Đính kèm theo thứ tự `valley_critter_apose_body_back.png`, `valley_critter_tpose_body.png`; lưu `valley_critter_tpose_body_back.png`:
```
Image 1 is the approved A-pose BACK view, Image 2 the approved T-pose FRONT view. Create the T-pose BACK view as one separate image: use Image 1 as the base and edit ONLY the arms, rotating them up to point straight out horizontally exactly like the arms in Image 2 (seen from behind). Everything else stays identical to Image 1.
```

#### Bảo bối

Mỗi đạo cụ một chat: đính kèm `<tên>_ref.png` của nó trong `Props/<Tên>/concept/`, gửi prompt trước (lưu `<tên>_front.png`), rồi prompt sau (lưu `<tên>_back.png`).

**Wonder Compass**
```
The attached image is the Wonder Compass, a magic prop from a soft stylized 3D animated film for young children. Create ONE image of exactly the same object seen straight from the front, orthographic, no perspective: the round gold case with the ring on top, the blue sky dial with white clouds and the glowing eight-pointed star needle (one point is the pointer: about one and a half times longer than the others, bright gold, with a small glowing blue gem at its tip; the other seven points are shorter, all the same length, pale white-blue, so the four points toward 12, 3, 6 and 9 o'clock are not longer than the diagonal ones and it never looks like a fixed compass rose; the pointer points to the upper right, about half past one on a clock, not at any gem or mark on the case), the blue diamond gems and the cream cloud ornament at the bottom of the case. Same design, colors and materials. Centered with some margin, square 1:1. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
```
Now the BACK view of the same object as one separate image: seen straight from behind, orthographic, same size and position in the frame. The back of the case is closed, smooth gold metal with a small engraved cloud swirl in the middle; the ring on top, the side gems and the cloud ornament seen from behind. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

**Inventor Pack**
```
The attached image is the Inventor Pack, Tavi's backpack in a soft stylized 3D animated film for young children. Create ONE image of exactly the same backpack seen straight from the front (the outer side that faces away from the wearer), orthographic, no perspective: blueprint roll and handle on top, flap with buckles, front pocket with the gold gear emblem, glowing crystal tubes on both sides, tool pocket with the wrench. Same design, colors and materials. Centered with some margin, square 1:1. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
```
Now the BACK view of the same backpack as one separate image: seen straight from behind, the side that rests against the wearer's back, orthographic, same size and position in the frame. A padded brown leather back panel with two padded shoulder straps and their gold buckles; the blueprint roll, the handle and the crystal tubes seen from behind. No gear emblem on this side. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

**Story Lens** (hình trong mặt kính thay theo từng manh mối, làm bằng shader, nên ảnh để kính trống)
```
The attached image is the Story Lens, a magic prop from a soft stylized 3D animated film for young children. Create ONE image of exactly the same object seen straight from the front, orthographic, no perspective, handle pointing straight down: round gold frame with white cloud ornaments, lilac crystal gems, the butterfly and crystal on top, purple handle with gold cloud details and a crystal at its end. The glass is clear with a soft lavender shimmer and NO picture inside. Same design, colors and materials. Centered with some margin, portrait 2:3. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
```
Now the BACK view of the same object as one separate image: seen straight from behind, orthographic, same size and position in the frame. The back of the gold frame, the butterfly, gems and cloud ornaments seen from behind, the handle from behind; the glass is clear with NO picture. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

**Pocket of Wonders** (Piko rút từng món ra, các món làm riêng, nên túi trống và thắt miệng như lúc đeo)
```
The attached image is the Pocket of Wonders, Piko's magic pouch in a soft stylized 3D animated film for young children. Create ONE image of exactly the same pouch seen straight from the front, orthographic, no perspective, as Piko wears it: purple velvet, its mouth gathered shut by the gold rope bow with the round blue gem, gold tassels on both sides, the cream cloud emblem with gold outline, the gold trim at the bottom. Nothing sticks out of the pouch: no bottle, crystal, mushroom, map, compass, feather, stars or sparkles. Centered with some margin, square 1:1. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
```
Now the BACK view of the same pouch as one separate image: seen straight from behind, orthographic, same size and position in the frame. Same purple velvet, the gold rope and tassels seen from behind, the gold trim at the bottom; plain velvet with no cloud emblem on this side. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

## Dựng trong Blender

Mỗi asset một build script dựng lưới, xương, face rig, material ra `<tên>_rig.blend` (`README.md`).

| | Thân (rig) | Làm riêng rồi gắn |
|---|---|---|
| **Lumo** | Thân 2 chân; xương tai; mặt | Áo choàng, túi đeo chéo, đuôi |
| **Tavi** | Thân 2 chân liền mũ, kính, gile ôm sát; gai tinh thể đi cứng theo ngực; mặt | Đuôi, Inventor Pack |
| **Nori** | Thân tròn, tay nhỏ, bay lơ lửng; mặt | 4 cánh trong suốt, 2 râu sao, vệt sáng thay chân |
| **Piko** | Thân co giãn bằng shape keys, tay nhỏ, sừng nảy; mặt | Pocket of Wonders: dây quàng gốc sừng phải, túi đung đưa theo cú nảy |
| **Sinh vật nhỏ** | Thân, tay chân ngắn | Lá khô đội đầu (trượt xuống che mắt, `valley_critters_ref.png`) |
| **Đôi voi con** | Thân 4 chân, vòi nắm được dây, tai; mặt. Voi thứ hai là bản đổi cỡ, tai, chỏm lông của voi thứ nhất | — |
| **Noah** | Chỉ dáng người và bàn tay; không rig mặt | — |

- **Mặt:** mắt, mí, đồng tử, lông mày là bộ phận rời gắn vào xương đầu; miệng là shape key bám trên bề mặt mõm; tất cả điều khiển bằng thanh trượt (custom property + driver) trên rig.
- **Lưới, texture:** quad, mỗi nhân vật dưới khoảng 50k mặt; texture 2048 là đủ (phim 1080p; 4096 nặng cho EEVEE trên Vega 11).
- Scale theo chiều cao trong Character Bible.
- Soát **bàn tay úp, ngón không dính nhau, miệng khép** trước khi rig.
- **Kiểm tra rig** trên các tư thế khó (giơ tay, bật nhảy, ngoái đầu, cúi), tư thế đặt theo trục thế giới: đo % diện tích mặt lưới bị bóp (< 40% so với tư thế nghỉ) hay giãn (> 250%), và tỉ lệ thể tích so với tư thế nghỉ. Đạt khi phần méo dưới khoảng 2%, thể tích gần 1.0.

### Gắn đồ rời (áo choàng, túi của Lumo; ba lô của Tavi)

Làm sau khi rig thân đã đạt kiểm tra.

| | Áo choàng | Túi đeo chéo / ba lô |
|---|---|---|
| Dựng | Theo `lumo_cape_ref.png`, đặt theo `lumo_outfit.png` và `lumo_outfit_back.png`. Lỗ cổ ôm mặt cắt vai; từ khuy trở xuống vạt áo rủ ra sau cánh tay (áo bọc kín quanh người thì tay đưa ra trước là áo phồng và nhăn) | Túi theo `lumo_bag_ref.png`: thân túi đặt trước bụng, lệch phải, đi cứng theo xương hông; dây dựng bằng code, vòng elip chéo từ hông phải qua vai trái, bám mặt da. Ba lô theo `inventor_pack_front.png`, `inventor_pack_back.png`, đặt theo `tavi_outfit_back.png` |
| Đi theo người | Chép trọng số da từ thân (Data Transfer), chỉ giữ ảnh hưởng của hông, lưng, ngực, cổ, vai; cánh tay 20%, đùi 30%; đầu, tai, đuôi, cẳng tay, cẳng chân không kéo áo | Dây: như áo choàng |

- **Áo choàng của Lumo dài tới gối** như concept. Đuôi mọc ở độ cao 0.2–0.3 m, thấp hơn mép áo, nên giữa lưng áo phải có khe xẻ cho đuôi thò ra. Chân bước dễ xuyên vạt áo, nên áo bắt buộc có xương vạt áo và va chạm với chân.
- **Kiểm tra:** đếm số đỉnh áo, dây lún vào người ở từng tư thế; giơ tay và chạy là hai tư thế dễ lún nhất.
- **Chưa có:** xương vạt áo (để áo bay khi chạy và tránh chân), khe đuôi, va chạm với chân, túi lắc theo bước. Mô phỏng vải (Cloth) chỉ dùng cho vài cận cảnh cần "wow" (áo quật trong bão): chậm, phải tính lại từng shot, dễ xuyên người.
