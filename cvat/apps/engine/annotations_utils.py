import requests

from cvat.apps.engine.models import (
    Label, Task, Organization
)

def generate_annotation_points(points):
    annotation_points =[]
    for x,y in zip(*[iter(points)]*2):
            value = {'x': x, 'y': y}
            annotation_points.append(value)
    return annotation_points

def save_annotations_to_polygon_backup(data, headers):
    tracks = data["tracks"]
    shapes = data["shapes"]
    for track in tracks:
        label_id = track['label_id']
        label = Label.objects.get(id = label_id)
        task = Task.objects.get(label__id = label_id)
        user_id = task.owner_id
        org_id = task.organization_id
        frame = track['shapes'][0]['frame']
        points = track['shapes'][0]['points']
        annotationPoints = generate_annotation_points(points)
        org = Organization.objects.get(id = org_id)
        json_data = {
            'annotationList': [
                {
                    'imageId': str(frame),
                    'orgId': str(org.id),
                    'taskId': str(task.id),
                    'objectName': label.name,
                    'annotationPolygonList': [
                        {
                            'annotationPoints': annotationPoints
                        },
                    ],
                },
            ],
        }
        requests.post(f'http://ec2co-ecsel-120oaoc0msxmg-363566620.us-east-1.elb.amazonaws.com:8081/images/user/{user_id}/org/{org.id}/task/{task.id}/image/{frame}/saveannotationfromcvat', headers=headers, json=json_data)

    for shape in shapes:
        label_id = shape['label_id']
        label = Label.objects.get(id = label_id)
        task = Task.objects.get(label__id = label_id)
        user_id = task.owner_id
        org_id = task.organization_id
        frame = shape['frame']
        points = shape['points']
        annotationPoints = []
        org = Organization.objects.get(id = org_id)
        annotationPoints = generate_annotation_points(points)
        json_data = {
            'annotationList': [
                {
                    'imageId': str(frame),
                    'orgId': str(org.id),
                    'taskId': str(task.id),
                    'objectName': label.name,
                    'annotationPolygonList': [
                        {
                            'annotationPoints': annotationPoints
                        },
                    ],
                },
            ],
        }
        requests.post(f'http://ec2co-ecsel-120oaoc0msxmg-363566620.us-east-1.elb.amazonaws.com:8081/images/user/{user_id}/org/{org.id}/task/{task.id}/image/{frame}/saveannotationfromcvat', headers=headers, json=json_data)

def save_annotations_to_polygon(data, headers):
    tracks = data["tracks"]
    shapes = data["shapes"]
    annotations_list = []

    for track in tracks:
        annotation_dict = {}
        annotations_point_list = [{}]
        label_id = track['label_id']
        label = Label.objects.get(id = label_id)
        task = Task.objects.get(label__id = label_id)
        user_id = task.owner_id
        org_id = task.organization_id
        org = Organization.objects.get(id = org_id)
        frame = track['shapes'][0]['frame']
        points = track['shapes'][0]['points']
        annotationPoints = generate_annotation_points(points)
        annotation_dict["imageId"] = str(frame)
        annotation_dict["orgId"] = str(org.id)
        annotation_dict["taskId"] = str(task.id)
        annotation_dict["objectName"] = label.name
        annotations_point_list[0]["annotationPoints"] = annotationPoints
        annotation_dict["annotationPolygonList"] = annotations_point_list
        annotations_list.append(annotation_dict)

    for shape in shapes:
        annotation_dict = {}
        annotations_point_list = [{}]
        label_id = track['label_id']
        label = Label.objects.get(id = label_id)
        task = Task.objects.get(label__id = label_id)
        user_id = task.owner_id
        org_id = task.organization_id
        org = Organization.objects.get(id = org_id)
        frame = shape['frame']
        points = shape['points']
        annotationPoints = generate_annotation_points(points)
        annotation_dict["imageId"] = str(frame)
        annotation_dict["orgId"] = str(org.id)
        annotation_dict["taskId"] = str(task.id)
        annotation_dict["objectName"] = label.name
        annotations_point_list[0]["annotationPoints"] = annotationPoints
        annotation_dict["annotationPolygonList"] = annotations_point_list
        annotations_list.append(annotation_dict)

    json_data = {'annotationList': annotations_list}
    requests.post(f'http://ec2co-ecsel-120oaoc0msxmg-363566620.us-east-1.elb.amazonaws.com:8081/images/user/{user_id}/org/{org.id}/task/{task.id}/image/{frame}/saveannotationfromcvat', headers=headers, json=json_data)
