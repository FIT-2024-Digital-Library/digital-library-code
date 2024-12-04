mc alias set local $MINIO_SERVER_HOSTNAME $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD
mc admin user add local $MINIO_LOGIN $MINIO_PASSWORD
mc admin policy attach local readwrite --user $MINIO_LOGIN
mc mb /mnt/minio-volume/$MINIO_BUCKET_NAME