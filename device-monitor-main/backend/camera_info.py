from onvif import ONVIFCamera

camera = ONVIFCamera(
    "10.45.0.2",
    8088,
    "admin",
    "admin123"
)

media = camera.create_media_service()

profiles = media.GetProfiles()

print("\n====== MEDIA PROFILES ======\n")

for p in profiles:
    print("--------------------------------")
    print("Name :", p.Name)
    print("Token:", p.token)