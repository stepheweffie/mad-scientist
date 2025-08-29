#!/bin/bash
# Docker management scripts for Mad Scientist AI

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if .env file exists
check_env_file() {
    if [ ! -f .env ]; then
        print_warning ".env file not found!"
        print_status "Creating .env file from template..."
        if [ -f .env.example ]; then
            cp .env.example .env
            print_warning "Please edit .env file with your configuration before running the application!"
            return 1
        else
            print_error ".env.example not found. Please create .env file manually."
            return 1
        fi
    fi
    return 0
}

# Build the Docker image
build() {
    print_status "Building Mad Scientist AI Docker image..."
    docker build -t mad-scientist:latest .
    print_success "Docker image built successfully!"
}

# Development environment
dev() {
    print_status "Starting Mad Scientist AI in development mode..."
    check_env_file || return 1
    
    docker-compose -f docker-compose.dev.yml up --build
}

# Development environment in background
dev_detached() {
    print_status "Starting Mad Scientist AI in development mode (detached)..."
    check_env_file || return 1
    
    docker-compose -f docker-compose.dev.yml up -d --build
    print_success "Development environment started in background!"
    print_status "View logs with: docker-compose -f docker-compose.dev.yml logs -f"
    print_status "Stop with: docker-compose -f docker-compose.dev.yml down"
}

# Production environment
prod() {
    print_status "Starting Mad Scientist AI in production mode..."
    check_env_file || return 1
    
    # Validate required environment variables
    if [ -z "$SECRET_KEY" ] || [ -z "$API_BASE_URL" ] || [ -z "$AUTH_TOKEN" ]; then
        print_error "Required environment variables missing!"
        print_status "Please ensure SECRET_KEY, API_BASE_URL, and AUTH_TOKEN are set in .env"
        return 1
    fi
    
    docker-compose -f docker-compose.prod.yml up -d --build
    print_success "Production environment started!"
    print_status "Application available at: http://localhost"
}

# Stop all containers
stop() {
    print_status "Stopping all Mad Scientist AI containers..."
    docker-compose -f docker-compose.yml down 2>/dev/null || true
    docker-compose -f docker-compose.dev.yml down 2>/dev/null || true
    docker-compose -f docker-compose.prod.yml down 2>/dev/null || true
    print_success "All containers stopped!"
}

# Clean up everything
clean() {
    print_status "Cleaning up Mad Scientist AI Docker resources..."
    
    # Stop containers
    stop
    
    # Remove images
    docker rmi mad-scientist:latest 2>/dev/null || true
    docker rmi $(docker images | grep mad-scientist | awk '{print $3}') 2>/dev/null || true
    
    # Remove volumes
    docker volume rm $(docker volume ls | grep mad | awk '{print $2}') 2>/dev/null || true
    
    # Prune unused resources
    docker system prune -f
    
    print_success "Cleanup completed!"
}

# View logs
logs() {
    local compose_file="docker-compose.yml"
    
    if [ -n "$1" ] && [ "$1" = "dev" ]; then
        compose_file="docker-compose.dev.yml"
    elif [ -n "$1" ] && [ "$1" = "prod" ]; then
        compose_file="docker-compose.prod.yml"
    fi
    
    print_status "Viewing logs from $compose_file..."
    docker-compose -f $compose_file logs -f
}

# Health check
health() {
    print_status "Checking Mad Scientist AI health..."
    
    local url="http://localhost:8000/health"
    local max_attempts=5
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        print_status "Health check attempt $attempt/$max_attempts..."
        
        if curl -f -s $url > /dev/null; then
            print_success "Application is healthy!"
            curl -s $url | python -m json.tool
            return 0
        fi
        
        sleep 2
        ((attempt++))
    done
    
    print_error "Application health check failed after $max_attempts attempts"
    return 1
}

# Shell into running container
shell() {
    local container_name="mad-scientist-app"
    
    if [ -n "$1" ]; then
        case "$1" in
            dev) container_name="mad-scientist-dev" ;;
            prod) container_name="mad-scientist-prod" ;;
        esac
    fi
    
    print_status "Opening shell in container: $container_name"
    docker exec -it $container_name /bin/bash
}

# Show usage
usage() {
    echo "Mad Scientist AI Docker Management Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  build           Build the Docker image"
    echo "  dev             Start in development mode (foreground)"
    echo "  dev-bg          Start in development mode (background)"
    echo "  prod            Start in production mode"
    echo "  stop            Stop all containers"
    echo "  clean           Stop containers and clean up resources"
    echo "  logs [env]      View logs (env: dev, prod, or default)"
    echo "  health          Check application health"
    echo "  shell [env]     Open shell in container (env: dev, prod, or default)"
    echo "  help            Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 dev          # Start development environment"
    echo "  $0 prod         # Start production environment"
    echo "  $0 logs dev     # View development logs"
    echo "  $0 shell prod   # Shell into production container"
}

# Main script logic
case "${1:-help}" in
    build)
        build
        ;;
    dev)
        dev
        ;;
    dev-bg)
        dev_detached
        ;;
    prod)
        prod
        ;;
    stop)
        stop
        ;;
    clean)
        clean
        ;;
    logs)
        logs $2
        ;;
    health)
        health
        ;;
    shell)
        shell $2
        ;;
    help|--help|-h)
        usage
        ;;
    *)
        print_error "Unknown command: $1"
        usage
        exit 1
        ;;
esac
