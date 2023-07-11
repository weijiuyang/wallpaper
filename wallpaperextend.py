import os 

def safework(wallpapers):
    path = os.path.join(os.path.dirname(__file__), 'static/images')
    print(path)
    images = os.listdir(path)
    print(images)
    imagelist = {}
    for image in images:
        prefix = image.split('.')[0]
        imagelist[prefix] = os.path.join(path.split('static/')[1],image) 
    print(imagelist)
    print('ttttttt')
    print(wallpapers)
    for paper in wallpapers:
        print(paper)
        print(paper.name)
        if paper.name in imagelist:
            paper.name = imagelist[paper.name]
    for one in wallpapers:
        print(one.name)
    return wallpapers



