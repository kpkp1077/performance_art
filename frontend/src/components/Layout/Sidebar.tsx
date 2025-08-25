import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Divider,
  Box,
  Typography,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  TrendingUp as DealsIcon,
  AttachMoney as CommissionsIcon,
  People as UsersIcon,
  Settings as SettingsIcon,
} from '@mui/icons-material';
import { User } from '../../types';

interface SidebarProps {
  open: boolean;
  onClose: () => void;
  drawerWidth: number;
  user: User;
}

const navigationItems = [
  {
    text: 'Dashboard',
    path: '/dashboard',
    icon: <DashboardIcon />,
    roles: ['admin', 'manager', 'rep'],
  },
  {
    text: 'Deals',
    path: '/deals',
    icon: <DealsIcon />,
    roles: ['admin', 'manager', 'rep'],
  },
  {
    text: 'Commissions',
    path: '/commissions',
    icon: <CommissionsIcon />,
    roles: ['admin', 'manager', 'rep'],
  },
  {
    text: 'Users',
    path: '/users',
    icon: <UsersIcon />,
    roles: ['admin', 'manager'],
  },
  {
    text: 'Settings',
    path: '/settings',
    icon: <SettingsIcon />,
    roles: ['admin'],
  },
];

const Sidebar: React.FC<SidebarProps> = ({ open, onClose, drawerWidth, user }) => {
  const location = useLocation();
  const navigate = useNavigate();

  const filteredItems = navigationItems.filter(item =>
    item.roles.includes(user.role)
  );

  const handleNavigation = (path: string) => {
    navigate(path);
  };

  const drawerContent = (
    <Box>
      <Toolbar />
      <Box sx={{ p: 2 }}>
        <Typography variant="body2" color="text.secondary">
          Role: {user.role.charAt(0).toUpperCase() + user.role.slice(1)}
        </Typography>
      </Box>
      <Divider />
      <List>
        {filteredItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton
              selected={location.pathname === item.path}
              onClick={() => handleNavigation(item.path)}
              sx={{
                '&.Mui-selected': {
                  backgroundColor: 'primary.main',
                  color: 'white',
                  '&:hover': {
                    backgroundColor: 'primary.dark',
                  },
                  '& .MuiListItemIcon-root': {
                    color: 'white',
                  },
                },
              }}
            >
              <ListItemIcon>
                {item.icon}
              </ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Box>
  );

  return (
    <Drawer
      variant="persistent"
      anchor="left"
      open={open}
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
        },
      }}
    >
      {drawerContent}
    </Drawer>
  );
};

export default Sidebar;