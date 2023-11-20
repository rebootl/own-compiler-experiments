#[derive(Debug, Clone)]
pub enum Element {
    Nil,
    Int(isize),
    // FLOAT(f64),
    // STRING(String),
}

impl Element {
    pub fn to_int(&self) -> isize {
        match self {
            Element::Nil => 0,
            Element::Int(i) => *i,
        }
    }
    pub fn add(&self, other: &Element) -> Option<Element> {
        match self {
            Element::Nil => None,
            Element::Int(i) => match other {
                Element::Nil => None,
                Element::Int(j) => Some(Element::Int(i + j)),
            },
        }
    }
    pub fn sub(&self, other: &Element) -> Option<Element> {
        match self {
            Element::Nil => None,
            Element::Int(i) => match other {
                Element::Nil => None,
                Element::Int(j) => Some(Element::Int(i - j)),
            },
        }
    }
    pub fn mul(&self, other: &Element) -> Option<Element> {
        match self {
            Element::Nil => None,
            Element::Int(i) => match other {
                Element::Nil => None,
                Element::Int(j) => Some(Element::Int(i * j)),
            },
        }
    }
    pub fn div(&self, other: &Element) -> Option<Element> {
        match self {
            Element::Nil => None,
            Element::Int(i) => match other {
                Element::Nil => None,
                Element::Int(j) => Some(Element::Int(i / j)),
            },
        }
    }
    pub fn neg(&self) -> Option<Element> {
        match self {
            Element::Nil => None,
            Element::Int(i) => Some(Element::Int(-i)),
        }
    }
}
