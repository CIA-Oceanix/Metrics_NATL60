def Taylor_diagram(list_data,labels_data,colors,lstyle,resfile):

    # select only 10-day windows
    index=list(range(5,16))
    index.extend(range(25,36))
    index.extend(range(45,56))
    index.extend(range(65,76))

    # apply High-Pass Filter to visualize Taylor diagrams only for small scales
    HR = list_data[2][index]
    lr = np.copy(HR).reshape(HR.shape[0],-1)
    tmp = lr[0,:]
    sea_v2 = np.where(~np.isnan(tmp))[0]
    lr_no_land = lr[:,sea_v2]
    pca = PCA(n_components=.75)
    score_global = pca.fit_transform(lr_no_land)
    coeff_global = pca.components_.T
    mu_global = pca.mean_
    DataReconstructed_global = np.dot(score_global, coeff_global.T) +mu_global
    lr[:,sea_v2] = DataReconstructed_global
    lr = lr.reshape(HR.shape).flatten()

    # create a dictionnary with data
    series={}
    for i in np.delete(np.arange(len(list_data)),1):
        series[labels_data[i]] = list_data[i][index].flatten()-lr
    Taylor_diag(series,np.delete(labels_data,1),\
            styles=np.delete(lstyle,1),\
            colors=np.delete(colors,1))
    plt.savefig(resfile)
    plt.close()

