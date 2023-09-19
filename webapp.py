
# client elasticsearch 
#query request : Fuzzy = Floue 
import streamlit as st
from elasticsearch import Elasticsearch

client = Elasticsearch("http://localhost:9200")

def fetch_initial_images(input, num_images):
    request = {
        "fuzzy": {"tags": input}
    }
    results = client.search(index="flk2", query=request)
    image_data = results["hits"]["hits"]
    
    # Fetch image URLs and create a list
    image_urls = [
        f"http://farm{hit['_source']['flickr_farm']}.staticflickr.com/"
        f"{hit['_source']['flickr_server']}/{hit['_source']['id']}_{hit['_source']['flickr_secret']}.jpg"
        for hit in image_data
    ]
    
    return image_urls[:num_images]

def fetch_more_images(input, start_index, num_images):
    request = {
        "fuzzy": {"tags": input}
    }
    results = client.search(index="flk2", query=request)
    image_data = results["hits"]["hits"]
    
    # Fetch image URLs and create a list
    image_urls = [
        f"http://farm{hit['_source']['flickr_farm']}.staticflickr.com/"
        f"{hit['_source']['flickr_server']}/{hit['_source']['id']}_{hit['_source']['flickr_secret']}.jpg"
        for hit in image_data
    ]
    
    return image_urls[start_index:start_index + num_images]

st.markdown('## Search Engine')
input = st.text_input("Write a word ")
search_button = st.button("Search")

if search_button:
    st.session_state.images = fetch_initial_images(input, 3)
    st.session_state.image_start_index = 3



# Display the images
if hasattr(st.session_state, "images") and st.session_state.images:
    columns = st.columns(3)
    
    for i, image_url in enumerate(st.session_state.images):
        columns[i % 3].image(image_url)



show_more_button = st.button("Show More")

if show_more_button:
    num_images_to_display = 3
    additional_images = fetch_more_images(input, st.session_state.image_start_index, num_images_to_display)
    if additional_images:
        st.session_state.images.extend(additional_images)
        st.session_state.image_start_index += num_images_to_display
