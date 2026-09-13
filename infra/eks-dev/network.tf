resource "aws_vpc" "eks" {
  cidr_block = var.vpc_cidr

  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "${local.name_prefix}-eks-vpc"
  }
}

resource "aws_internet_gateway" "eks" {
  vpc_id = aws_vpc.eks.id

  tags = {
    Name = "${local.name_prefix}-eks-igw"
  }
}

resource "aws_subnet" "public" {
  for_each = var.public_subnets

  vpc_id            = aws_vpc.eks.id
  cidr_block        = each.value.cidr_block
  availability_zone = each.value.availability_zone

  # Public worker networking avoids a continuously billed NAT gateway in this
  # temporary development environment. It is not the production target design.
  # trivy:ignore:AWS-0164
  map_public_ip_on_launch = true

  tags = {
    Name = "${local.name_prefix}-${each.key}"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.eks.id

  tags = {
    Name = "${local.name_prefix}-public-rt"
  }
}

resource "aws_route" "internet" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.eks.id
}

resource "aws_route_table_association" "public" {
  for_each = aws_subnet.public

  subnet_id      = each.value.id
  route_table_id = aws_route_table.public.id
}
