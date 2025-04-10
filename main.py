# Libraries
import pandas as pd
import numpy as np
import math
from scipy import stats
from sklearn.metrics import davies_bouldin_score
import streamlit as st

import plotly.express as px
import matplotlib.pyplot as plt
from PIL import Image

from datetime import date
from datetime import datetime


def main():

    # Session Handling
    if 'data' not in st.session_state:
        st.session_state.data = pd.DataFrame()
    
    if 'arfm' not in st.session_state:
        st.session_state.arfm = pd.DataFrame()

    if 'data_kmeans' not in st.session_state:
        st.session_state.data_kmeans = pd.DataFrame()

    if 'data_kmedoids' not in st.session_state:
        st.session_state.data_kmedoids = pd.DataFrame()

    if 'jumlah_cluster' not in st.session_state:
        st.session_state.jumlah_cluster = 2

    if 'df_ARFM2' not in st.session_state:
        st.session_state.df_ARFM2 = pd.DataFrame()

    # Main Interface
    img = Image.open('polos.png')
    st.image(img, width=200)
    st.markdown(f'<h1 style="color:#E37236;font-size:48px;">{"TRAINCLUST"}</h1>', unsafe_allow_html=True)
    st.header('_:brown[Aplikasi Cluster Training Pelayaran POLTEKPEL BANTEN]_')
    st.write("""
             Aplikasi ini digunakan untuk mengelompokkan peserta jasa training/sertifikasi pelayaran baik taruna/alumni POLTEKPEL BANTEN.
             Metode yang digunakan antara lain KMeans dan KMedoids berdasarkan fitur Age, Recency, Frequency, Monetary.
             """)
    
    # Sidebar Initiation
    st.sidebar.title("Pilih Menu")
    menu0 = st.sidebar.selectbox("Data:", ["Pilih", "Dataset", "Analisis"])
    menu1 = st.sidebar.selectbox("Training:", ["Pilih", "Cluster"])
    menu2 = st.sidebar.selectbox("Evaluasi", ["Pilih", "Hasil Cluster"])

    if menu0 == "Dataset" and menu1 == "Pilih" and menu2 == "Pilih":
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            #read excel
            st.session_state.data=pd.read_excel(uploaded_file, engine='openpyxl')

            #processing
            st.session_state.data['Tanggal Lahir'] = pd.to_datetime(st.session_state.data['Tanggal Lahir'])
            st.session_state.data['Age'] = (datetime.today() - st.session_state.data['Tanggal Lahir'])
            for i in range(len(st.session_state.data)):
                st.session_state.data['Age'][i] = int(st.session_state.data['Age'][i].days / 365)
            st.session_state.data = st.session_state.data.drop(['Unnamed: 0'], axis=1)
            st.session_state.data['NRT/Kode Pelaut'] = st.session_state.data['NRT/Kode Pelaut'].astype(str)
            st.session_state.data = st.session_state.data.drop(["Usia"], axis=1)

            # st.session_state.data['Tanggal Lahir'] = pd.to_datetime(st.session_state.data['Tanggal Lahir'])
            # st.session_state.data['Tanggal Transaksi'] = pd.to_datetime(st.session_state.data['Tanggal Transaksi'])

            st.session_state.data['Tanggal Lahir'] = st.session_state.data['Tanggal Lahir'].dt.date
            st.session_state.data['Tanggal Transaksi'] = st.session_state.data['Tanggal Transaksi'].dt.date
            # st.session_state.data['Tanggal Lahir'] = pd.to_datetime(st.session_state.data['Tanggal Lahir'])
            # st.session_state.data['Tanggal Transaksi'] = pd.to_datetime(st.session_state.data['Tanggal Transaksi'])
   
            #view
            st.dataframe(st.session_state.data)

            st.session_state.data['Tanggal Lahir'] = pd.to_datetime(st.session_state.data['Tanggal Lahir'])
            st.session_state.data['Tanggal Transaksi'] = pd.to_datetime(st.session_state.data['Tanggal Transaksi'])
   

    if menu0 == "Analisis" and menu1 == "Pilih" and menu2 == "Pilih":
        # plot the number of customers each day
        fig = plt.figure(figsize=(15,5))
        df_sales_n_user=st.session_state.data.resample("D",on='Tanggal Transaksi')['NRT/Kode Pelaut'].nunique()
        df_sales_n_user.rename('Jumlah Taruna/Alumni', inplace=True)
        df_sales_n_user.index = [item.date() for item in df_sales_n_user.index]

        st.subheader("Jumlah Taruna / Alumnni")
        st.dataframe(df_sales_n_user)

        # Create  plot
        fig = px.line(df_sales_n_user,
            x = df_sales_n_user.index,
            y = "Jumlah Taruna/Alumni",
            title = f"Jumlah Taruna/Alumni",
            )
                    
        # Plot
        st.plotly_chart(fig, use_container_width=True)


        a=st.session_state.data.resample('M',on='Tanggal Transaksi')['Nominal Transaksi'].sum().to_frame()
        a['month']=['Jun','Jul','Aug',"Sep", "Oct", "Nov", "Dec", "Jan\n2023", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"]
        a['Nominal Transaksi']=a['Nominal Transaksi']/1000000
        a.index = [item.date() for item in a.index]

        st.subheader("Nominal Transaksi")
        st.dataframe(a)

        # Create  plot
        fig = px.bar(a,
            x = a.index,
            y = "Nominal Transaksi",
            title = f"total transaksi (juta Rp)",
            text_auto='.2s',
            )
                    
        # Plot
        st.plotly_chart(fig, use_container_width=True)


        df_sales_p_day=st.session_state.data.resample('D',on='Tanggal Transaksi')['Nominal Transaksi'].sum()
        df_sales_spent=df_sales_p_day/df_sales_n_user
        df_sales_spent.rename('Average Transaksi Per Alumni (Juta Rupiah)', inplace=True)
        df_sales_spent.index = [item.date() for item in df_sales_spent.index]



        st.subheader("Average Biaya Diklat per Taruna atau Alumni")
        st.dataframe(df_sales_spent)

        # Create  plot
        fig = px.area(df_sales_spent,
            x = df_sales_spent.index,
            y = "Average Transaksi Per Alumni (Juta Rupiah)",
            title = f"average biaya diklat/taruna atau alumni (Rp)",
            )
                    
        # Plot
        st.plotly_chart(fig, use_container_width=True)


    if menu0 == "Pilih" and menu1 == "Cluster" and menu2 == "Pilih":
        # step 0 calculate "Age"
        df_A = st.session_state.data.groupby('NRT/Kode Pelaut')['Age'].mean().reset_index().rename(columns={"Age":"Age"})
        # step 1 calculate "Recency"
        latest_date = st.session_state.data['Tanggal Transaksi'].max()
        st.session_state.data['Duration to Latest Date'] = latest_date - st.session_state.data['Tanggal Transaksi']
        st.session_state.data['Duration to Latest Date'] = pd.to_numeric(st.session_state.data['Duration to Latest Date'].dt.days, downcast='integer')
        st.session_state.data['Recency'] = st.session_state.data['Duration to Latest Date']
        df_R = st.session_state.data.groupby('NRT/Kode Pelaut')['Recency'].min().reset_index().rename(columns={"0":"Recency"})
        # step 2 calculate "Frequency"
        df_F = st.session_state.data.groupby('NRT/Kode Pelaut')['Diklat'].count().reset_index().rename(columns={"Diklat":"Frequency"})
        # step 3 calculate "Monetary"
        df_M = st.session_state.data.groupby('NRT/Kode Pelaut')["Nominal Transaksi"].sum().reset_index().rename(columns={"Nominal Transaksi":"Monetary"})
        # step 4 merge "Age", "Recency", "Frequency", "Monetary"
        df_AR = pd.merge(df_A, df_R, on='NRT/Kode Pelaut')
        df_ARF = pd.merge(df_AR, df_F, on='NRT/Kode Pelaut')
        df_ARFM = pd.merge(df_ARF, df_M, on='NRT/Kode Pelaut')

        conditions=np.abs(stats.zscore(df_ARFM.loc[:,['Recency','Frequency','Monetary']]) < 3).all(axis=1)
        st.session_state.df_ARFM2=df_ARFM.loc[conditions,:]

        st.subheader("Age - Recency - Frequency - Monetary")
        st.dataframe(st.session_state.df_ARFM2)

        # Create  plot
        fig = px.histogram(st.session_state.df_ARFM2,
                x = ["Age"],
                title = f"Age Cluster",
                )
                        
        # Plot
        st.plotly_chart(fig, use_container_width=True)

        # Create  plot
        fig = px.histogram(st.session_state.df_ARFM2,
                x = ["Recency"],
                title = f"Recency",
                )
                        
        # Plot
        st.plotly_chart(fig, use_container_width=True)

        # Create  plot
        fig = px.histogram(st.session_state.df_ARFM2,
                x = ["Frequency"],
                title = f"Frequency",
                )
                        
        # Plot
        st.plotly_chart(fig, use_container_width=True)


        # Create  plot
        fig = px.histogram(st.session_state.df_ARFM2,
                x = ["Monetary"],
                title = f"Monetary",
                )
                        
        # Plot
        st.plotly_chart(fig, use_container_width=True)


        #KMEANS

        class KMeansClustering:
            def __init__(self, X, num_clusters):
                self.K = num_clusters # cluster number
                self.max_iterations = 100 # max iteration. don't want to run inf time
                self.num_examples, self.num_features = X.shape # num of examples, num of features
                self.plot_figure = True # plot figure
                
            # randomly initialize centroids
            def initialize_random_centroids(self, X):
                centroids = np.zeros((self.K, self.num_features)) # row , column full with zero 
                for k in range(self.K): # iterations of 
                    centroid = X[np.random.choice(range(self.num_examples))] # random centroids
                    centroids[k] = centroid
                return centroids # return random centroids
            
            # create cluster Function
            def create_cluster(self, X, centroids):
                clusters = [[] for _ in range(self.K)]
                for point_idx, point in enumerate(X):
                    closest_centroid = np.argmin(
                        np.sqrt(np.sum((point-centroids)**2, axis=1))
                    ) # closest centroid using euler distance equation(calculate distance of every point from centroid)
                    clusters[closest_centroid].append(point_idx)
                return clusters 
            
            # new centroids
            def calculate_new_centroids(self, cluster, X):
                centroids = np.zeros((self.K, self.num_features)) # row , column full with zero
                for idx, cluster in enumerate(cluster):
                    new_centroid = np.mean(X[cluster], axis=0) # find the value for new centroids
                    centroids[idx] = new_centroid
                return centroids
            
            # prediction
            def predict_cluster(self, clusters, X):
                y_pred = np.zeros(self.num_examples) # row1 fillup with zero
                for cluster_idx, cluster in enumerate(clusters):
                    for sample_idx in cluster:
                        y_pred[sample_idx] = cluster_idx
                return y_pred
            
            # plotinng scatter plot
            def plot_fig(self, X, y):
                fig = px.scatter(X[:, 0], X[:, 1], color=y)
                fig.show() # visualize
                
            # fit data
            def fit(self, X):
                centroids = self.initialize_random_centroids(X) # initialize random centroids
                for _ in range(self.max_iterations):
                    clusters = self.create_cluster(X, centroids) # create cluster
                    previous_centroids = centroids
                    centroids = self.calculate_new_centroids(clusters, X) # calculate new centroids
                    diff = centroids - previous_centroids # calculate difference
                    if not diff.any():
                        break
                y_pred = self.predict_cluster(clusters, X) # predict function
                # if self.plot_figure: # if true
                #     self.plot_fig(X, y_pred) # plot function 
                return y_pred
            
        # KMEDOIDS
        
        def euclideanDistance(x, y):
            '''
            Euclidean distance between x, y
            --------
            Return
            d: float
            '''
            squared_d = 0
            for i in range(len(x)):
                squared_d += (x[i] - y[i])**2
            d = np.sqrt(squared_d)
            return d
            
        class k_medoids:
            def __init__(self, k = 2, max_iter = 300, has_converged = False):
                ''' 
                Class constructor
                Parameters
                ----------
                - k: number of clusters. 
                - max_iter: number of times centroids will move
                - has_converged: to check if the algorithm stop or not
                '''
                self.k = k
                self.max_iter = max_iter
                self.has_converged = has_converged
                self.medoids_cost = []
                
            def initMedoids(self, X):
                ''' 
                Parameters
                ----------
                X: input data. 
                '''
                self.medoids = []
                
                #Starting medoids will be random members from data set X
                indexes = np.random.randint(0, len(X)-1,self.k)
                self.medoids = X[indexes]
                
                for i in range(0,self.k):
                    self.medoids_cost.append(0)
                
            def isConverged(self, new_medoids):
                '''
                Parameters
                ----------
                new_medoids: the recently calculated medoids to be compared with the current medoids stored in the class
                '''
                return set([tuple(x) for x in self.medoids]) == set([tuple(x) for x in new_medoids])
                
            def updateMedoids(self, X, labels):
                '''
                Parameters
                ----------
                labels: a list contains labels of data points
                '''
                self.has_converged = True
                
                #Store data points to the current cluster they belong to
                clusters = []
                for i in range(0,self.k):
                    cluster = []
                    for j in range(len(X)):
                        if (labels[j] == i):
                            cluster.append(X[j])
                    clusters.append(cluster)
                
                #Calculate the new medoids
                new_medoids = []
                for i in range(0, self.k):
                    new_medoid = self.medoids[i]
                    old_medoids_cost = self.medoids_cost[i]
                    # print(f"medoids {i}: {new_medoid}")
                    for j in range(len(clusters[i])):
                        
                        #Cost of the current data points to be compared with the current optimal cost
                        cur_medoids_cost = 0
                        for dpoint_index in range(len(clusters[i])):
                            cur_medoids_cost += euclideanDistance(clusters[i][j], clusters[i][dpoint_index])
                        
                        #If current cost is less than current optimal cost,
                        #make th c.e current data point new medoid of the cluster
                        if cur_medoids_cost < old_medoids_cost:
                            new_medoid = clusters[i][j]
                            old_medoids_cost = cur_medoids_cost
                    
                    #Now we have the optimal medoid of the current cluster
                    new_medoids.append(new_medoid)
                # print(f"medoids cost: {cur_medoids_cost}")
                
                #If not converged yet, accept the new medoids
                if not self.isConverged(new_medoids):
                    self.medoids = new_medoids
                    self.has_converged = False
            
            def fit(self, X):
                '''
                FIT function, used to find clusters
                Parameters
                ----------
                X: input data. 
                '''
                self.initMedoids(X)
                
                for i in range(self.max_iter):
                    # print(f"Iterasi ke - {i}")
                    #Labels for this iteration
                    cur_labels = []
                    for medoid in range(0,self.k):
                        #Dissimilarity cost of the current cluster
                        self.medoids_cost[medoid] = 0
                        for k in range(len(X)):
                            #Distances from a data point to each of the medoids
                            d_list = []                    
                            for j in range(0,self.k):
                                d_list.append(euclideanDistance(self.medoids[j], X[k]))
                            #Data points' label is the medoid which has minimal distance to it
                            cur_labels.append(d_list.index(min(d_list)))
                            
                            self.medoids_cost[medoid] += min(d_list)
                                        
                    self.updateMedoids(X, cur_labels)
                    
                    if self.has_converged:
                        break

                return np.array(self.medoids)

                
            def predict(self,data):
                ''' 
                Parameters
                ----------
                data: input data.
                
                Returns:
                ----------
                pred: list cluster indexes of input data 
                '''
            
                pred = []
                for i in range(len(data)):
                    #Distances from a data point to each of the medoids
                    d_list = []
                    for j in range(len(self.medoids)):
                        d_list.append(euclideanDistance(self.medoids[j],data[i]))
                        
                    pred.append(d_list.index(min(d_list)))
                    
                return np.array(pred)
            
        # Preparing input training
        df_ARFM3=st.session_state.df_ARFM2.drop(columns=['NRT/Kode Pelaut'])
        X = np.array(df_ARFM3.astype(int))

        select = st.selectbox("Pilih Metode:", 
            ["Pilih",
            "KMEANS",
            "KMEDOIDS", 
            ])
        st.session_state.jumlah_cluster = st.number_input("Masukkan Jumlah Cluster: ", min_value=2, step=1)
        butt_training = st.button("Mulai Training")
        
        if select == "KMEANS" and butt_training:
            model = KMeansClustering(X, num_clusters=st.session_state.jumlah_cluster)
            # model.fit(X)
            st.success("Training KMeans Selesai.")
            df_ARFM3['cluster'] = model.fit(X)
            st.session_state.data_kmeans = df_ARFM3.copy(deep = True)
            st.session_state.data_kmeans = pd.concat([st.session_state.df_ARFM2[["NRT/Kode Pelaut"]], st.session_state.data_kmeans], axis=1)
            st.dataframe(st.session_state.data_kmeans)
            
            # Hitung Davies Bouldin Index
            davies_bouldin_scores = []
            for k in range(2, 5):
                    km = KMeansClustering(X, num_clusters=k)
                    labels = km.fit(X) # Labeling
                    score = davies_bouldin_score(X, labels)
                    davies_bouldin_scores.append(score)
                
            df_score = pd.DataFrame(
                    {"Cluster": range(2, 5), 
                    "Davies Score": davies_bouldin_scores
                    }
                                    )
            # Create scatter plot
            fig = px.line(df_score,
                                x = "Cluster",
                                y = "Davies Score",
                                title = "Davies Bouldin Score")
                                      
            # Plot
            st.plotly_chart(fig, use_container_width=True)

        if select == "KMEDOIDS" and butt_training:
            model = k_medoids(k=st.session_state.jumlah_cluster)
            model.fit(X)
            st.success("Training KMedoids Selesai.")
            df_ARFM3['cluster'] = model.predict(X)
            st.session_state.data_kmedoids = df_ARFM3.copy(deep = True)
            st.session_state.data_kmedoids = pd.concat([st.session_state.df_ARFM2[["NRT/Kode Pelaut"]], st.session_state.data_kmedoids], axis=1)
            st.dataframe(st.session_state.data_kmedoids)

            # Hitung Davies Bouldin Index
            davies_bouldin_scores = []
            for k in range(2, 5):
                    kmed = k_medoids(k=k)
                    kmed.fit(X)
                    labels = kmed.predict(X) # Labeling
                    score = davies_bouldin_score(X, labels)
                    davies_bouldin_scores.append(score)
                
            df_score = pd.DataFrame(
                    {"Cluster": range(2, 5), 
                    "Davies Score": davies_bouldin_scores
                    }
                                    )
            # Create scatter plot
            fig = px.line(df_score,
                                x = "Cluster",
                                y = "Davies Score",
                                title = "Davies Bouldin Score")
            
            # Plot
            st.plotly_chart(fig, use_container_width=True)

    if menu0 == "Pilih" and menu1 == "Pilih" and menu2 == "Hasil Cluster":
        meth = st.selectbox("Pilih Method", ["KMEANS", "KMEDOIDS"])
        cl = st.selectbox("Pilih Cluster", range(st.session_state.jumlah_cluster))

        if meth == "KMEANS":
            df_c = st.session_state.data_kmeans[st.session_state.data_kmeans['cluster'] == int(cl)]
            st.dataframe(df_c)
            # Create  plot
            fig = px.histogram(df_c,
                x = ["Age"],
                title = f"Age Cluster {int(cl)}",
                )
                        
            # Plot
            st.plotly_chart(fig, use_container_width=True)

                        # Create  plot
            fig = px.histogram(df_c,
                x = ["Recency"],
                title = f"Recency Cluster {int(cl)}",
                )
                        
            # Plot
            st.plotly_chart(fig, use_container_width=True)

            # Create  plot
            fig = px.histogram(df_c,
                x = ["Frequency"],
                title = f"Frequency Cluster {int(cl)}",
                )
                        
            # Plot
            st.plotly_chart(fig, use_container_width=True)


            # Create  plot
            fig = px.histogram(df_c,
                x = ["Monetary"],
                title = f"Monetary Cluster {int(cl)}",
                )
                        
            # Plot
            st.plotly_chart(fig, use_container_width=True)

        if meth == "KMEDOIDS":
            df_c = st.session_state.data_kmedoids[st.session_state.data_kmedoids['cluster'] == int(cl)]
            st.dataframe(df_c)

            # Create  plot
            fig = px.histogram(df_c,
                x = ["Age"],
                title = f"Age Cluster {int(cl)}",
                )
                        
            # Plot
            st.plotly_chart(fig, use_container_width=True)

            # Create  plot
            fig = px.histogram(df_c,
                x = ["Recency"],
                title = f"Recency Cluster {int(cl)}",
                )
                        
            # Plot
            st.plotly_chart(fig, use_container_width=True)

            # Create  plot
            fig = px.histogram(df_c,
                x = ["Frequency"],
                title = f"Frequency Cluster {int(cl)}",
                )
                        
            # Plot
            st.plotly_chart(fig, use_container_width=True)


            # Create  plot
            fig = px.histogram(df_c,
                x = ["Monetary"],
                title = f"Monetary Cluster {int(cl)}",
                )
                        
            # Plot
            st.plotly_chart(fig, use_container_width=True)



# Running program
if __name__ == "__main__":
    main()

