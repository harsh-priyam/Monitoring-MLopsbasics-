RUN echo '#!/bin/bash' > /code/entrypoint.sh && \
    echo 'pip install -e .' >> /code/entrypoint.sh && \
    echo 'python src/driver.py' >> /code/entrypoint.sh && \
    echo 'cd /code && python main.py' >> /code/entrypoint.sh && \
    chmod +x /code/entrypoint.sh