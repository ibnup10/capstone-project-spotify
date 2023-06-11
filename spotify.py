import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from PIL import Image
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

st.set_page_config(
    page_title= 'Rekomendasi lagu K-Pop  berdasarkan Audio feature Spotify',
    layout='wide'
)

data = pd.read_csv('top10_girlband_based_on_seoulbox.csv')
data['length'] = data['length']/1000 #Merubah satuan lagu menjadi detik/second
df=data.drop('Unnamed: 0', axis=1)

img = 'https://myseoulbox.com/cdn/shop/articles/Copy_of_Seoulbox_Blog_Banner_b17971a7-6a04-45e9-b061-dcf273038a58.png?v=1678851321&width=1100'
st.markdown(f"<div style='display: flex; justify-content: center;'><img src='{img}' width='1200'></div>", unsafe_allow_html=True)
st.write('')
st.divider()

st.markdown("<h3 style='text-align: center;'>Latar Belakang</h1>", unsafe_allow_html=True)

with st.expander(label='Lihat Penjelasan'):
    st.markdown(
    """
    <div style="text-align: justify;">
        <p>Pada Pandemi COVID-19 seluruh masyarakat Indonesia memilih untuk beraktifitas dari rumah, otomatis gawai pun jadi senjata untuk berkomunikasi, menjelajah internet. Mulai dari TikTok, Twitter, Instagram, YouTube dan sebagainya. Tidak bisa keluar rumah akhirnya konten-konten apapun diikuti sebagai penghilang stress, termasuk dari konten dari Negeri Ginseng atau Korea Selatan,mulai dari K-Drama maupun K-pop. Menurut AntaraNews, penyebaran gelombang Korea (Korean wave) menjadi sangat cepat dan masif sejak masyarakat dunia harus beraktivitas dari rumah dan melakukan pembatasan sosial dalam skala besar. Mereka yang sebelumnya tidak tahu menahu mengenai Korea, kini mulai tertarik bahkan mengikuti berbagai hal yang berhubungan dengan Negeri Ginseng tersebut. Dalam hal ini saya telah merangkum 10 Girl Group K-pop terbaik Tahun 2023 menurut MySeoulbox dan menganalisis 5 lagu setiap 10 Girl Group tersebut dalam 3 tahun terakhir yang diambil melalui Aplikasi Spotify dengan Audio Feature milik Spotify.</p>
        <p>Semua data musik diambil melalui Aplikasi Streaming Musik yaitu Spotify melalui API dari Developer Spotify. Ada bebearapa informasi yang diambil meliput Track dan Audio Feature untuk menganalisis. Track meliputi Judul Lagu,Album,Artist,Tanggal Rilis,Durasi,dan Popularitas. Sementara Audio Feature meliputi Danceability, Acousticness, Energy, Instrumentalness, Loudness, Speechiness, Liveness, Tempo, Time Signature.</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

st.markdown("<h3 style='text-align: center;'>Popularitas Girl Group pada Tahun 2023</h1>", unsafe_allow_html=True)

col1, col2= st.columns(2)
# Menambahkan garis tengah pada kolom 1
col1.markdown("<style>div.stButton > button {border-right: 1px solid #FF0000;}</style>", unsafe_allow_html=True)
# Menambahkan garis tengah pada kolom 2
col2.markdown("<style>div.stButton > button {border-left: 1px solid #FF0000;}</style>", unsafe_allow_html=True)

# Chart 1 - Girl Group Popularity

with col1:
        popularity_data = df.groupby('artist')['popularity'].mean().reset_index()
        popularity_data = popularity_data.sort_values('popularity', ascending=False)
        chart = alt.Chart(popularity_data).mark_bar().encode(
        x=alt.X('artist:N', sort=None),
        y=alt.Y('popularity:Q', scale=alt.Scale(domain=(0, 100))),
        tooltip=['artist', 'popularity'],
        color=alt.Color('artist:N', scale=alt.Scale(scheme='category20'))
    ).properties(
        title={
            'text': 'Girl Group Chart Popularity 2023 ',
            'fontSize': 16,
            'align': 'center',
            'anchor': 'middle'
        },
        width=600,
        height=400
    ).configure_legend(
        disable=True
    )
    
st.altair_chart(chart, use_container_width=True)
with st.expander('Popularitas Girl Group berdasarkan Artist'):
        st.markdown(
    """
    <div style="text-align: justify;">
        <p>Pada chart diatas dijelaskan bahwa ada 10 Girl Group menurut MySeoulBox. Bisa kita lihat, perolehan tertinggi dipimpin oleh Girl Group bernama 'NewJeans' dengan perolehan popularitas sebesar 86.4, dengan 5 besar teratars diikuti oleh IVE, LE SSERAFIM, aespa, dan BLACKPINK. Kepopuleran ini dihitung rata-rata popularity spotify setiap 5 lagu dalam 3 tahun terakhir pada Girl Group masing-masing</p>
    </div>
    """,
    unsafe_allow_html=True
)  
        st.markdown(
    """
    <div style="text-align: justify;">
        <p>Perlu diketahui bahwa NewJeans adalah Girl Group pendatang baru yang baru debut di Tahun 2022 dengan single "Attention" dan ditahun itu juga mereka mendapatkan Best New Artist pada tahun 2022 Melon Music Awards. Namun,mengapa namanya begitu cepat melesit dan bisa menempati top chart di Tahun 2023?</p>
    </div>
    """,
    unsafe_allow_html=True
)

sorted_data = data.sort_values('popularity', ascending=False)
top_songs = sorted_data.head(5)
pivot_table = pd.pivot_table(top_songs, values='popularity', index=['name', 'artist'], aggfunc=max).reset_index()
pivot_table['rank'] = pivot_table['popularity'].rank(method='first', ascending=False).astype(int)  # Menambahkan kolom rank
pivot_table = pivot_table.sort_values('rank') # Mengurutkan berdasarkan kolom rank
pivot_table.insert(0, 'Peringkat', pivot_table['rank'])  # Memasukkan kolom "Rank" di posisi pertama
pivot_table = pivot_table.drop(columns='rank')
pivot_table = pivot_table.rename(columns={'name': 'Lagu', 'artist': 'Artis', 'popularity': 'Kepopuleran'})
table_title = table_title = "<h3 style='font-size: 16px; text-align:center; margin:auto'>Top 5 Song Girl Group K-pop on 2023</h3>"
st.markdown(table_title, unsafe_allow_html=True)
pivot_table_style = pivot_table.style.set_table_styles(
        [{
        'selector': 'table',
        'props': [
            ('text-align', 'center'),  # Mengatur teks menjadi tengah
            ('margin', 'auto'),  # Mengatur margin menjadi auto untuk pusat secara horizontal
            ('display', 'block'),  # Mengatur tampilan tabel menjadi block untuk pusat secara vertikal
        ]
        }]
    )
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
st.markdown(hide_table_row_index, unsafe_allow_html=True)

st.table(pivot_table_style)
with st.expander('Popularitas Girl Group Berdasarkan Lagu'):
    st.markdown(
    """
    <div style="text-align: justify;">
        <p>Ternyata Girl Group dibawah naungan HYBE LABES yaitu NewJeans memimpin dengan 3 lagu nya di 5 lagu teratas di tahun 2023, dan dua diantaranya datang dari Girl Group IVE dan LE SSERAFIM yang berduet dengan Nile Rodgers. Peringkat pertama dipimpin oleh NewJeans dengan lagunya yaitu "OMG". Dilansir oleh Hanteo Chart, penjualan Single Album “OMG” terjual lebih dari 480.000 eksemplar pada penjualan hari pertamanya saja. Lagu ini sering digunakan ataupun didengar dengan video-video di TikTok untuk dance cover</p>
    </div>
    """,
    unsafe_allow_html=True
)
    st.markdown(
    """
    <div style="text-align: justify;">
        <p>Jika anda ingin mendengarkan lagu ini, berikut dibawah ini adalah preview dari NewJeans-OMG beserta streaming dari Spotify atau YouTube.</p>
    </div>
    """,
    unsafe_allow_html=True
)
    
with st.expander("Preview for No.1 K-pop Girl Group song On 2023"):
    st.markdown(
    """
    <style>
    .centered-text {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)
    st.markdown("<h1 style='text-align: center;'>NewJeans - OMG</h1>", unsafe_allow_html=True)
    image = 'https://i.scdn.co/image/ab67616d0000b273d70036292d54f29e8b68ec01'
    st.markdown(f"<div style='display: flex; justify-content: center;'><img src='{image}' width='150'></div>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; font-size: 12px;'>Stream here</h2>", unsafe_allow_html=True)
    st.markdown(
    """
    <div style='text-align: center; display: flex; justify-content: center; margin-top: -10px'>
        <a href='https://open.spotify.com/intl-id/track/65FftemJ1DbbZ45DUfHJXE?si=070cbdb76e3748b3'>
            <img src='https://cdn.icon-icons.com/icons2/836/PNG/32/Spotify_icon-icons.com_66783.png' alt='Gambar 1'>
        </a>
        <a href='https://www.youtube.com/watch?v=sVTy_wmn5SU'>
            <img src='https://cdn.icon-icons.com/icons2/1211/PNG/32/1491580651-yumminkysocialmedia28_83061.png' alt='Gambar 2'>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
    table_container = st.container()
    with table_container:
        audio_file = open('D:/belajar_streamlit/NJOMG.mp3', 'rb')
        st.audio(audio_file, format='audio/mp3')

st.divider()

st.markdown("<h3 style='text-align: center;'>Korelasitas antar Audio Feature</h1>", unsafe_allow_html=True)

#Corelation Heatmap
df_corr = df[['length', 'danceability', 'acousticness', 'energy', 'instrumentalness', 'loudness', 'speechiness', 'liveness', 'tempo', 'time_signature']]
corr_matrix = df_corr.corr().reset_index().melt('index')



# Membuat heatmap
heatmap = alt.Chart(corr_matrix).mark_rect().encode(
    alt.X('index:O',title='Audio Features'),
    y='variable:O',
    color='value:Q'
).properties(
        title={
            'text': ' Correlation Heatmap',
            'fontSize': 16,
            'align': 'center',
            'anchor': 'middle'
        },
        width=600,
        height=600
)

# Menambahkan teks di dalam kotak heatmap
text = alt.Chart(corr_matrix).mark_text(baseline='middle').encode(
    x='index:O',
    y='variable:O',
    text=alt.Text('value:Q', format='.2f'),
    color=alt.condition(
        alt.datum.value > 0.5,  # Menentukan kondisi teks berwarna hitam jika value > 0.5
        alt.value('black'),
        alt.value('white')
    )
)

# Menggabungkan heatmap dengan teks
heatmap_with_text = (heatmap + text)    
col1,col2,col3=st.columns([0.5,1,0.5])
with col2:
    st.altair_chart(heatmap_with_text)
# Menampilkan heatmap
with st.expander('Korelasi antar audio feature'):
    
    st.markdown(
    """
    <div style="text-align: justify;">
        <p>Pada heatmap Korelasi tersebut bisa menjadi ukuran untuk menentukan bahwa dari audio yang dihasilkan musik saling memiliki keterkaitan salah satunya menentukan Genre Music, bisa jadi genre pada suatu lagu memiliki lebih dari satu genre, kita ketahui bahwa K-Pop memiliki variasi-variasi genre. Korelasi negatif diatas bukan berarti tidak ada sambungan antar audio fitur, melainkan nilai negatif menunjukan antara fitur audio dan genre musik, itu berarti terdapat hubungan kebalikan antara fitur audio tersebut dengan genre-genre yang diamati. Misalnya, jika terdapat korelasi negatif antara kecepatan tempo dengan acousticness, hal itu dapat menunjukkan bahwa audio feature yang memiliki acousticnes tersebut cenderung memiliki tempo yang lebih lambat. Semua audio fitur memiliki nilai range 0-1. </p>
    </div>
    """,
    unsafe_allow_html=True
)


## Preprocessing
# Menghapus kolom yang tidak perlu
df_drop = df.drop(['name', 'album', 'artist', 'release_date', 'popularity'], axis=1)
# Membuat objek StandardScaler
scaler = StandardScaler(copy=True)
# Melakukan scaling pada data
df2 = pd.DataFrame(scaler.fit_transform(df_drop), columns=df_drop.columns)
# Menampilkan dataframe hasil scaling

## Implementasi Clustering K-Means
wcss = []
for i in range(1, 11):
    model = KMeans(n_clusters=i, init='k-means++', n_init=10, max_iter=1000, random_state=42)
    model.fit(df2)
    wcss.append(model.inertia_)
elbow_data = pd.DataFrame({'Number of Clusters': range(1, 11), 'WCSS': wcss})

elbow_chart = alt.Chart(elbow_data).mark_line().encode(
    x='Number of Clusters',
    y='WCSS'
).properties(
        title={
            'text': ' Elbow Chart',
            'fontSize': 16,
            'align': 'center',
            'anchor': 'middle'
        },
        width=500,
        height=300
)


col1,col2,col3 = st.columns([0.5,1,0.5])
with col2:
    st.altair_chart(elbow_chart)
with st.expander('Cluster Genre'):
    st.markdown(
    """
    <div style="text-align: justify;">
        <p>Elbow chart diatas adalah metode clustering untuk genre yang akan dibagi lagi menjadi rasio cluster berdasarkan audio fitur. Dari hasil elbow chart diatas, saya mengambil 4 cluster genre berdasarkan audio fitur yaitu Energy, Danceabilty, Acousticness, dan Tempo.</p>
    </div>
    """,
    unsafe_allow_html=True
)

kmeans = KMeans(n_clusters=5, init='k-means++',max_iter=500, n_init=10,random_state=0)
y_kmeans = kmeans.fit_predict(df2)
df['cluster'] = y_kmeans
df1= df[['length', 'popularity', 'danceability', 'acousticness', 'energy', 'instrumentalness', 'loudness', 'speechiness', 'liveness', 'tempo', 'time_signature','cluster']]

clus_0 = df1[df1["cluster"]==0]
#clus_1 = df1[df1["cluster"]==1]
clus_2 = df1[df1["cluster"]==2]
clus_3 = df1[df1["cluster"]==3]
clus_4 = df1[df1["cluster"]==4]

df_result = pd.DataFrame(clus_0.mean(),columns=['Hip Hop']) #Danceabilty
#df_result.insert(1, 'Ballad', clus_1.mean()) #instrumentalness
df_result.insert(1, 'R&B Pop', clus_2.mean()) #Acousticness
df_result.insert(2, 'Dance Pop', clus_3.mean()) #Energy
df_result.insert(3, 'Pop', clus_4.mean()) #Tempo


# Menggabungkan subset data-frame menjadi satu tabel
combined_df = pd.concat([clus_0, clus_2, clus_3, clus_4])
# Mapping antara cluster dan genre
genre_mapping = {
    0: 'Hip Hop',
    2: 'R&B Pop',
    3: 'Dance Pop',
    4: 'Pop',
}

st.divider()
st.markdown("<h2 style='text-align: center;'>Rasio antar audio fitur</h2>", unsafe_allow_html=True)
st.write('')


# Mengubah kolom cluster menjadi genre
combined_df['genre'] = combined_df['cluster'].map(genre_mapping)



tabs1, tabs2, tabs3, tabs4 =st.tabs(['Energy', 'Danceability', 'Acousticness','Tempo'])
# Membuat plot menggunakan Altair
with tabs1:
    with st.container():
        energy= alt.Chart(combined_df).mark_circle(size=100).encode(
        x=alt.X('energy', title='Energy'),
        y=alt.Y('length', title='Length'),
        color=alt.Color('genre:N', scale=alt.Scale(scheme='category10'), legend=alt.Legend(title='Genre', labelFontSize=12))
).properties(
        title={
            'text': 'Rasio antara Energy dan Length',
            'fontSize': 16,
            'align': 'center',
            'anchor': 'middle'
        }
).interactive()
        col1,col2,col3=st.columns(3)   
        with col2:
            st.altair_chart(energy)
    with st.expander('Lihat Penjelasan'):
     st.markdown(
    """
    <div style="text-align: justify;">
        <p>Pada rasio diatas audio fitur yang dibandingkah adalah energy dan length atau durasi lagu, bisa disumpulkan bahwa rasio dari dance pop sangat terlihat berdekatan pada jarak nilai 0.8-0.9, ini berarti mendekati 1 menandakan bahwa lagu-lagu yang memiliki energi yang sangat aktif dan intensitas yang kuat masuk ke Kategori Dance Pop dan bisa digunakan untuk lagu beraktifitas seperti senam, lari, maupun aktifitas olahraga laiinnya, bisa juga untuk menemani teman kerja anda agar selalu produktif dan semangat ataupun kegiatan positive vibes lainnya. </p>
    </div>
    """,
    unsafe_allow_html=True
)
    with st.expander('Rekomendasi lagu'):
        col1, col2, col3 = st.columns(3)
        with col1: 
            st.markdown("<h1 style='text-align: center; font-size: 16px;'>TWICE - Talk That Talk</h1>", unsafe_allow_html=True)
            image = 'https://i.scdn.co/image/ab67616d00001e02c3040848e6ef0e132c5c8340'
            st.markdown(f"<div style='display: flex; justify-content: center;'><img src='{image}' width='150'></div>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; font-size: 12px;'>Stream here</h2>", unsafe_allow_html=True)
            st.markdown(
    """
    <div style='text-align: center; display: flex; justify-content: center; margin-top: -10px'>
        <a href='https://open.spotify.com/intl-id/track/0RDqNCRBGrSegk16Avfzuq'>
            <img src='https://cdn.icon-icons.com/icons2/836/PNG/32/Spotify_icon-icons.com_66783.png' alt='Gambar 1'>
        </a>
        <a href='https://youtu.be/k6jqx9kZgPM'>
            <img src='https://cdn.icon-icons.com/icons2/1211/PNG/32/1491580651-yumminkysocialmedia28_83061.png' alt='Gambar 2'>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
        with col2:
            st.markdown("<h1 style='text-align: center; font-size: 16px;'> IVE - After LIKE </h1>", unsafe_allow_html=True)
            image = 'https://i.scdn.co/image/ab67616d00001e0287f53da5fb4ab1171766b2d5'
            st.markdown(f"<div style='display: flex; justify-content: center;'><img src='{image}' width='150'></div>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; font-size: 12px;'>Stream here</h2>", unsafe_allow_html=True)
            st.markdown(
    """
    <div style='text-align: center; display: flex; justify-content: center; margin-top: -10px'>
        <a href='https://open.spotify.com/intl-id/track/2gYj9lubBorOPIVWsTXugG?si=6d3cd34a86a8487e'>
            <img src='https://cdn.icon-icons.com/icons2/836/PNG/32/Spotify_icon-icons.com_66783.png' alt='Gambar 1'>
        </a>
        <a href='https://youtu.be/k6jqx9kZgPM'>
            <img src='https://cdn.icon-icons.com/icons2/1211/PNG/32/1491580651-yumminkysocialmedia28_83061.png' alt='Gambar 2'>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
        with col3:
            st.markdown("<h1 style='text-align: center; font-size: 16px;'> MAMAMOO - Dingga </h1>", unsafe_allow_html=True)
            image = 'https://i.scdn.co/image/ab67616d00001e02b4fd0ba98f675df97c5748b1'
            st.markdown(f"<div style='display: flex; justify-content: center;'><img src='{image}' width='150'></div>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; font-size: 12px;'>Stream here</h2>", unsafe_allow_html=True)
            st.markdown(
    """
    <div style='text-align: center; display: flex; justify-content: center; margin-top: -10px'>
        <a href='https://open.spotify.com/intl-id/track/0bDYceyQd1jnJO4sK47YxU?si=d8d28313f14a4b06'>
            <img src='https://cdn.icon-icons.com/icons2/836/PNG/32/Spotify_icon-icons.com_66783.png' alt='Gambar 1'>
        </a>
     <a href='https://youtu.be/dfl9KIX1WpU'>
            <img src='https://cdn.icon-icons.com/icons2/1211/PNG/32/1491580651-yumminkysocialmedia28_83061.png' alt='Gambar 2'>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
            st.write('')

with tabs2:
    with st.container():
        dance= alt.Chart(combined_df).mark_circle(size=100).encode(
         x=alt.X('danceability', title='Danceability'),
         y=alt.Y('length', title='Length'),
         color=alt.Color('genre:N', scale=alt.Scale(scheme='category10'), legend=alt.Legend(title='Genre', labelFontSize=12))
).properties(
    title='Rasio Cluster Berdasarkan Danceability dan Length'
).interactive()
    col1, col2, col3 = st.columns(3)
    with col2:
        st.altair_chart(dance)
    with st.expander('Lihat Penjelasan'):
     st.markdown(
    """
    <div style="text-align: justify;">
        <p>Rasio kali ini yang dibandingkan adalah fitur Danceability dengan Length. Terlihat Rasio dot dengan berwarna oranye atau musik yang bergenre hip hop memiliki dominasi berkumpul berdekatan berbaris ke atas di jarak 0.7-0.86 dengan length yang bervariasi, semantara Dance Pop berpencar ditengah namun masih berkaitan dengan satu sama lain dot dance pop lainnya. Hal ini menunjukan bahwa lagu Hip Hop memiliki keterkaitan yang sesuai untuk digunakan sebagai lagu "Dance". Lagu ini bisa digunakan untuk kegiatan Freestyle Dance ataupun Koreografi Dance</p>
    </div>
    """,
    unsafe_allow_html=True
)
    with st.expander('Rekomendasi lagu'):
        col1, col2, col3 = st.columns(3)
        with col1: 
            st.markdown("<h1 style='text-align: center; font-size: 16px;'>BLACKPINK - 'Typa girl'</h1>", unsafe_allow_html=True)
            image = 'https://i.scdn.co/image/ab67616d00001e02580ac3ad7dfc81e509171120'
            st.markdown(f"<div style='display: flex; justify-content: center;'><img src='{image}' width='150'></div>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; font-size: 12px;'>Stream here</h2>", unsafe_allow_html=True)
            st.markdown(
    """
    <div style='text-align: center; display: flex; justify-content: center; margin-top: -10px'>
        <a href='https://open.spotify.com/intl-id/track/3BHR1mJOqn2UZyq98YKPgd?si=090af0853b8f4721'>
            <img src='https://cdn.icon-icons.com/icons2/836/PNG/32/Spotify_icon-icons.com_66783.png' alt='Gambar 1'>
        </a>
        <a href='https://youtu.be/UhxW9Njqqu0'>
            <img src='https://cdn.icon-icons.com/icons2/1211/PNG/32/1491580651-yumminkysocialmedia28_83061.png' alt='Gambar 2'>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
        with col2:
            st.markdown("<h1 style='text-align: center; font-size: 16px;'> LE SSERAFIM - ANTIFRAGILE </h1>", unsafe_allow_html=True)
            image = 'https://i.scdn.co/image/ab67616d00001e02a991995542d50a691b9ae5be'
            st.markdown(f"<div style='display: flex; justify-content: center;'><img src='{image}' width='150'></div>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; font-size: 12px;'>Stream here</h2>", unsafe_allow_html=True)
            st.markdown(
    """
    <div style='text-align: center; display: flex; justify-content: center; margin-top: -10px'>
        <a href='https://open.spotify.com/intl-id/track/4fsQ0K37TOXa3hEQfjEic1?si=945290d8473e448b'>
            <img src='https://cdn.icon-icons.com/icons2/836/PNG/32/Spotify_icon-icons.com_66783.png' alt='Gambar 1'>
        </a>
        <a href='https://youtu.be/pyf8cbqyfPs'>
            <img src='https://cdn.icon-icons.com/icons2/1211/PNG/32/1491580651-yumminkysocialmedia28_83061.png' alt='Gambar 2'>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
            with col3:
                st.markdown("<h1 style='text-align: center; font-size: 16px;'> NewJeans - Cookie </h1>", unsafe_allow_html=True)
                image = 'https://i.scdn.co/image/ab67616d00001e029d28fd01859073a3ae6ea209'
                st.markdown(f"<div style='display: flex; justify-content: center;'><img src='{image}' width='150'></div>", unsafe_allow_html=True)
                st.markdown("<h2 style='text-align: center; font-size: 12px;'>Stream here</h2>", unsafe_allow_html=True)
                st.markdown(
    """
    <div style='text-align: center; display: flex; justify-content: center; margin-top: -10px'>
        <a href='https://open.spotify.com/intl-id/track/2DwUdMJ5uxv20EhAildreg?si=dcc99c62dd634cf6'>
            <img src='https://cdn.icon-icons.com/icons2/836/PNG/32/Spotify_icon-icons.com_66783.png' alt='Gambar 1'>
        </a>
     <a href='https://youtu.be/VOmIplFAGeg'>
            <img src='https://cdn.icon-icons.com/icons2/1211/PNG/32/1491580651-yumminkysocialmedia28_83061.png' alt='Gambar 2'>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
        st.write('')

with tabs3:
    with st.container():
        acoustic= alt.Chart(combined_df).mark_circle(size=100).encode(
        x=alt.X('acousticness', title='Acoustic'),
        y=alt.Y('length', title='Length'),
        color=alt.Color('genre:N', scale=alt.Scale(scheme='category10'), legend=alt.Legend(title='Genre', labelFontSize=12))
).properties(
    title='Rasio Cluster Berdasarkan Acoustic dan Length'
).interactive()
    col1, col2, col3 = st.columns(3)
    with col2:
     st.altair_chart(acoustic)
    with st.expander('Lihat Penjelasan'):
     st.markdown(
    """
    <div style="text-align: justify;">
        <p>Di Rasio yang ketiga, kali ini yang dibandingkan adalah acoustic dan length. 'acousticness' adalah salah satu fitur atau atribut yang digunakan dalam analisis audio pada pemrosesan musik. Ini mengindikasikan sejauh mana lagu tersebut memiliki elemen akustik dalam produksinya. Pada rasio table diatas semua genre berkumpul pada value 0.1-0.2 namun dot berwarna merah yang mewakili R&B Pop berada di range 0.3-0.4 walau ada jarak namun sedikit berdekatan. R&B Pop bisa jadi untuk rekomendasi lagu santai anda atau lagu ketika menghadapi macet dijalan agar selalu santai dan pikiran tenang.</p>
    </div>
    """,
    unsafe_allow_html=True
)
    with st.expander('Rekomendasi lagu'):
        col1, col2, col3 = st.columns(3)
        with col1: 
            st.markdown("<h1 style='text-align: center; font-size: 16px;'>aespa - 'Thirsty'</h1>", unsafe_allow_html=True)
            image = 'https://i.scdn.co/image/ab67616d00001e0204878afb19613a94d37b29ce'
            st.markdown(f"<div style='display: flex; justify-content: center;'><img src='{image}' width='150'></div>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; font-size: 12px;'>Stream here</h2>", unsafe_allow_html=True)
            st.markdown(
    """
    <div style='text-align: center; display: flex; justify-content: center; margin-top: -10px'>
        <a href='https://open.spotify.com/intl-id/track/6nICBdDevG4NZysIqDFPEa?si=267b3fd05588458b'>
            <img src='https://cdn.icon-icons.com/icons2/836/PNG/32/Spotify_icon-icons.com_66783.png' alt='Gambar 1'>
        </a>
        <a href='https://youtu.be/i0RCcSBPjuU'>
            <img src='https://cdn.icon-icons.com/icons2/1211/PNG/32/1491580651-yumminkysocialmedia28_83061.png' alt='Gambar 2'>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
        with col2:
            st.markdown("<h1 style='text-align: center; font-size: 16px;'> LE SSERAFIM - Sour Grapes </h1>", unsafe_allow_html=True)
            image = 'https://i.scdn.co/image/ab67616d00001e029030184114911536d5f77555'
            st.markdown(f"<div style='display: flex; justify-content: center;'><img src='{image}' width='150'></div>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; font-size: 12px;'>Stream here</h2>", unsafe_allow_html=True)
            st.markdown(
    """
    <div style='text-align: center; display: flex; justify-content: center; margin-top: -10px'>
        <a href='https://open.spotify.com/intl-id/track/6wBpO4Xc4YgShnENGSFA1M?si=e9da1deb02ca420a'>
            <img src='https://cdn.icon-icons.com/icons2/836/PNG/32/Spotify_icon-icons.com_66783.png' alt='Gambar 1'>
        </a>
        <a href='https://youtu.be/V9Wsm0hlLUI'>
            <img src='https://cdn.icon-icons.com/icons2/1211/PNG/32/1491580651-yumminkysocialmedia28_83061.png' alt='Gambar 2'>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
    with col3:
        st.markdown("<h1 style='text-align: center; font-size: 16px;'> Red Velvet - Bye Bye </h1>", unsafe_allow_html=True)
        image = 'https://i.scdn.co/image/ab67616d00001e02d2ef237da7f94762997c2083'
        st.markdown(f"<div style='display: flex; justify-content: center;'><img src='{image}' width='150'></div>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; font-size: 12px;'>Stream here</h2>", unsafe_allow_html=True)
        st.markdown(
    """
    <div style='text-align: center; display: flex; justify-content: center; margin-top: -10px'>
        <a href='https://open.spotify.com/intl-id/track/4OSVR8gq2l3ceJiXNR7iiM?si=8a607b4717144f72'>
            <img src='https://cdn.icon-icons.com/icons2/836/PNG/32/Spotify_icon-icons.com_66783.png' alt='Gambar 1'>
        </a>
     <a href='https://youtu.be/TPNUscDJvew'>
            <img src='https://cdn.icon-icons.com/icons2/1211/PNG/32/1491580651-yumminkysocialmedia28_83061.png' alt='Gambar 2'>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
        st.write('')

with tabs4:
    with st.container():
        tempo= alt.Chart(combined_df).mark_circle(size=100).encode(
         x=alt.X('tempo', title='Tempo'),
         y=alt.Y('length', title='Length'),
    color=alt.Color('genre:N', scale=alt.Scale(scheme='category10'), legend=alt.Legend(title='Genre', labelFontSize=12))
).properties(
    title='Rasio Cluster Berdasarkan Tempo dan Length'
).interactive()
        col1, col2, col3 = st.columns(3)
    with col2:
     st.altair_chart(tempo)
    with st.expander('Lihat Penjelasan'):
        st.markdown(
    """
    <div style="text-align: justify;">
        <p>Rasio ini membandingan dengan tempo dan length. Tempo dalam musik merujuk pada kecepatan atau kecepatan pergerakan musik. Ini mengacu pada seberapa cepat atau lambat irama musik diputar atau dilakukan yang ditentukan oleh jumlah ketuman Beats per Minute (BPM). Lagu pada tempo yang cepat cocok untuk kegiatan beraktifitas seperti membersihkan rumah, olahraga, atau digunakan juga untuk mengekspresikan rasa senang, sedangkan tempo lambat digunakan untuk mengekspresikan rasa sedih atau galau akan sesatu yang telah dilalui. Rasio diatas menunjukan Ketiga genre dengan range 100bpm-160bpm, sedangkan Pop memilik lebih dari 150bpm-180bpm berkumpul di keatas dengan length yang bervariasi. Dibawah ini ada rekomendasi 3 lagu dengan Tempo Sedang, Lambat, dan Cepat</p>
    </div>
    """,
    unsafe_allow_html=True
)
    with st.expander('Rekomendasi lagu'):
        col1, col2, col3 = st.columns(3)
        with col1: 
            st.markdown("<h1 style='text-align: center; font-size: 16px;'>MAMAMOO - AYA</h1>", unsafe_allow_html=True)
            image = 'https://i.scdn.co/image/ab67616d00001e021cc469da4da1bccfa16867be'
            st.markdown(f"<div style='display: flex; justify-content: center;'><img src='{image}' width='150'></div>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; font-size: 12px;'>Stream here</h2>", unsafe_allow_html=True)
            st.markdown(
    """
    <div style='text-align: center; display: flex; justify-content: center; margin-top: -10px'>
        <a href='https://open.spotify.com/intl-id/track/4BZXVFYCb76Q0Klojq4piV?si=50f68cc19dc842e2'>
            <img src='https://cdn.icon-icons.com/icons2/836/PNG/32/Spotify_icon-icons.com_66783.png' alt='Gambar 1'>
        </a>
        <a href='https://youtu.be/UoI9riNffEU'>
            <img src='https://cdn.icon-icons.com/icons2/1211/PNG/32/1491580651-yumminkysocialmedia28_83061.png' alt='Gambar 2'>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
        with col2:
            st.markdown("<h1 style='text-align: center; font-size: 16px;'> TWICE - THE FEELS </h1>", unsafe_allow_html=True)
            image = 'https://i.scdn.co/image/ab67616d00001e02d1961ecb307c9e05ec8f7e82'
            st.markdown(f"<div style='display: flex; justify-content: center;'><img src='{image}' width='150'></div>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; font-size: 12px;'>Stream here</h2>", unsafe_allow_html=True)
            st.markdown(
    """
    <div style='text-align: center; display: flex; justify-content: center; margin-top: -10px'>
        <a href='https://open.spotify.com/intl-id/track/308Ir17KlNdlrbVLHWhlLe?si=40d8874f120d4083'>
            <img src='https://cdn.icon-icons.com/icons2/836/PNG/32/Spotify_icon-icons.com_66783.png' alt='Gambar 1'>
        </a>
        <a href='https://youtu.be/f5_wn8mexmM'>
            <img src='https://cdn.icon-icons.com/icons2/1211/PNG/32/1491580651-yumminkysocialmedia28_83061.png' alt='Gambar 2'>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
        with col3:
            st.markdown("<h1 style='text-align: center; font-size: 16px;'> BLACKPINK - Venom </h1>", unsafe_allow_html=True)
            image = 'https://i.scdn.co/image/ab67616d00001e02580ac3ad7dfc81e509171120'
            st.markdown(f"<div style='display: flex; justify-content: center;'><img src='{image}' width='150'></div>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; font-size: 12px;'>Stream here</h2>", unsafe_allow_html=True)
            st.markdown(
    """
    <div style='text-align: center; display: flex; justify-content: center; margin-top: -10px'>
        <a href='https://open.spotify.com/intl-id/track/5P3o95Jf0YBQRQ4j2XPpfC?si=509450d2cf7b4932'>
            <img src='https://cdn.icon-icons.com/icons2/836/PNG/32/Spotify_icon-icons.com_66783.png' alt='Gambar 1'>
        </a>
     <a href='https://youtu.be/gQlMMD8auMs'>
            <img src='https://cdn.icon-icons.com/icons2/1211/PNG/32/1491580651-yumminkysocialmedia28_83061.png' alt='Gambar 2'>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
            st.write('')

st.divider()

with st.container():
    st.markdown("<h2 style='text-align: center; font-size: 12px;'>Kontak Saya</h2>", unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    with c2:
     st.markdown(
    """
    <div style='text-align: center; display: flex; justify-content: center; margin-top: -10px'>
        <a href='https://www.linkedin.com/in/ibnup10/'>
            <img src='https://img.icons8.com/?size=32&id=13930&format=png' alt='Gambar 1'>
        </a>
        <a href='https://github.com/reznovka'>
            <img src='https://img.icons8.com/?size=32&id=63777&format=png' alt='Gambar 2'>
        </a>
        <a href='mailto:ibnupangestu1998@gmail.com'>
            <img src='https://img.icons8.com/?size=32&id=P7UIlhbpWzZm&format=png' alt='Gambar 2'>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)


with st.sidebar:
    st.title('Sumber Data:')
    st.write("[Developer Spotify](https://developer.spotify.com/)")
    st.write('[AntaraNews](https://www.antaranews.com/interaktif/semua-demam-korea-pada-waktunya/index.html)')
    st.write('[MySeoulBox Blog](https://myseoulbox.com/blogs/seoul-blog/best-k-pop-girls-groups-in-2023)')

