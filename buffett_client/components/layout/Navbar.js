import React from "react";
import { Button, Dropdown, Space } from "antd";
import css from "styled-jsx/css";

const items = [
  {
    key: "1",
    label: <div>모든 자산배분전략</div>,
  },
  {
    key: "2",
    label: <div>BAA</div>,
  },
];

const Navbar = () => {
  return (
    <div className="wrapper">
      <Dropdown
        menu={{
          items,
        }}
        placement="bottomLeft"
      >
        <Button type="primary">자산배분 전략</Button>
      </Dropdown>
      <style jsx>{SNavbar}</style>
    </div>
  );
};

const SNavbar = css`
  .wrapper {
    height: 4.75rem;
    padding: 1rem 2rem;
    box-sizing: border-box;
    display: flex;
    -webkit-box-pack: center;
    justify-content: center;
    background-color: rgb(34, 34, 34);
    border-bottom: 1px solid;
  }
`;

export default Navbar;
